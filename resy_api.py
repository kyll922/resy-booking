import re
import requests
import tomllib
import getpass


class ResyApi:
    def __init__(self, config, auth_token=None):

        self.payment_method = None
        self.auth_token = auth_token
        self.api_key = config['api_key']
        self.party_size = config['party_size']
        self.booking_time = config['booking_time']
        self.booking_date = config['booking_date']
        self.venue_url = config['venue_url']
        self.desired_seating = config['desired_seating']

        self.headers = {
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "authorization": self.api_key,
            "referer": "https://resy.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/131.0.0.0 Safari/537.36",
        }

        self.__login(config['file_path'])

    def __login(self, file_path: str = None):
        """
        Logs into resy using the supplied credentials, grabbing the users API auth token.
        :param file_path: The file path passed for configs.toml
        :return: auth_token & payment_method
        """
        print('.....Logging in.....')

        if file_path:
            with open(file_path, 'r') as file:
                data = tomllib.loads(file.read())

            email = data['credentials'].get('user_name') or input("Email: ")
            password = data['credentials'].get('password') or getpass.getpass()

        else:
            print("File path not found, exiting.")
            exit()

        body = {"email": email, "password": password}
        response = requests.post('https://api.resy.com/3/auth/password', headers=self.headers, data=body)
        response_data = response.json()

        if response.status_code == 200:
            print("Successfully logged in")
        else:
            print(f"Response Code: {response_data["status"]}\n"
                  f"Message: {response_data["message"]}\n"
                  f"Exiting...")
            exit()

        self.auth_token = response_data["token"]
        self.payment_method = response_data["payment_method_id"]
        self.headers["x-resy-auth-token"] = self.auth_token

        return self.auth_token, self.payment_method

    def get_venue_id(self) -> int | None:
        """
        For non-technical users to paste the URL landing page of the restaurant they wish to book at, and get the
        venue_id that is required.
        :param url: The URL found by going to resy.com, clicking your favorite restaurant, and copy + paste the URL
        from the address bar of the browser.
        :return: The venue_id, or None if unavailable.
        """
        headers = {
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "authorization": self.api_key,
            "referer": "https://resy.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-resy-auth-token": self.auth_token
        }

        pattern = r"/cities/([^/]+)/venues/([^/?]+)"
        match = re.search(pattern, self.venue_url)

        if match:
            location = match.group(1)  # "city-state"
            venue_name = match.group(2)  # "name-of-venue"
        else:
            print("Error grabbing the venue ID from the URL, please try again. Exiting.")
            exit()

        endpoint = f'https://api.resy.com/3/venue?url_slug={venue_name}&location={location}'
        response = requests.get(endpoint, headers=headers)
        data = response.json()
        if data:
            return data['id']['resy']

    def get_config_token(self, venue_id: int) -> str | None:
        """
        Gets the configuration token required for booking.
        :param venue_id: The int ID of the venue you wish to book.
        some venues offer selections such as "bar". This will allow you to input the string you see under the times on
        that page. The method will try to find a time with that seating type, otherwise it will default to "Dining Room"
        :return:
        """

        headers = {
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "authorization": self.api_key,
            "referer": "https://resy.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/131.0.0.0 Safari/537.36",
            "x-resy-auth-token": self.auth_token
        }

        response = requests.get(
            f'https://api.resy.com/4/find?lat=0&long=0&day={self.booking_date}&party_size={self.party_size}&venue_id={venue_id}',
            headers=headers)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results")

            if results is None:
                return None

            open_slots = results["venues"][0]["slots"]

            openings = [slot for slot in open_slots]
            if openings:
                best_config_found = None
                for config_item in openings:
                    if self.booking_date and self.booking_time in config_item['date']['start']:

                        # Check to see if preferred dining is available (names are on booking pages when select time),
                        # defaults to 'Dining Room'.
                        if self.desired_seating in config_item['config']['type']:
                            # payment_info = config_item['payment']
                            return config_item['config']['token']

                        else:
                            # if we need cancellation fee info etc., - placeholder
                            # payment_info = config_item['payment']
                            best_config_found = config_item['config']['token']

                return best_config_found

        else:
            return f"Server Response: {response.status_code}"

    def make_reservation(self, config) -> bool:
        """
        Books the found reservation.
        :param config: booking_token
        :return: bool
        """

        params = {
            'config_id': config,
            'day': self.booking_date,
            'party_size': self.party_size
        }

        response = requests.get('https://api.resy.com/3/details', headers=self.headers, params=params)
        booking_details = response.json()

        if not booking_details.get("book_token"):
            print("No booking token available. Please try again. Exiting.")
            exit()
        else:
            booking_token = booking_details["book_token"].get("value")

            data = {'book_token': booking_token}

            response = requests.post('https://api.resy.com/3/book', headers=self.headers, data=data)

            res = response.json()

            if res.get("reservation_id"):
                return True

            if res.get("specs"):
                print("reservation for this spot already exists")
                print("DETAILS: ", res["specs"])
                return False
