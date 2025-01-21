# Workflow for the booking.
import time
import helper
import resy_api


def main():
    print("-------------------------------------------------\n"
          "Avoid running multiple times in short notice, as resy.com will temporarily block the account for "
          "excessive login attempts.\n\n"
          "Instructions:\n"
          "1. Fill out information on the configs.toml file under [reservation_details] if desired, or put values as "
          "false only.\n"
          "2. Paste the file path of the configs.toml file when prompted.\n"
          "3. Fill out the required data when prompted if the configs.toml file was left with false values.\n"
          "4. Enter login information for resy.com.\n"
          "5. Once logged in the app will take over, simply wait until a slot becomes available. This will run in the "
          "background until the desired date and time is found and booked. You can stop it at any time.\n"
          "6. Sign into resy.com through the browser to ensure your reservation is showing.\n"
          "-------------------------------------------------\n\n")

    config = helper.config_parser()
    conn = resy_api.ResyApi(config)
    venue_id = conn.get_venue_id()

    # Once all the details are in place, we can loop indefinitely until the time and date is posted for reservation.
    # In the future we may add a "target time" to the config to fire an HTTP request at x time.
    found_config = False
    attempts = 0
    while found_config is False:
        try:
            helper.print_progress(10)
            config = conn.get_config_token(venue_id=venue_id)
            if config:
                found_config = True

            time.sleep(2)

            if config and 'Server Response: ' in config:
                if attempts >= 10:
                    print("Server connection attempt failed too many times, please retry. Exiting.")
                    exit()
                attempts += 1

        except Exception as e:
            print(e)
            exit()

    print('\rNow booking')
    booking = conn.make_reservation(config)

    if booking:
        print("Success! Please login to the browser to check details.")

    else:
        print("Failed to grab the booking token, please try again.")


if __name__ == '__main__':
    main()
