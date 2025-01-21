import getpass
import sys
from datetime import datetime
import tomllib


def valid_date() -> str:
    """
    Ensures the target date entered is validated as YYYY-MM-DD
    :return: valid date as str
    """
    while True:
        date_input = input("Desired booking date (YYYY-MM-DD): ")
        try:
            validated_date = datetime.strptime(date_input, "%Y-%m-%d")
            return validated_date.date().strftime('%Y-%m-%d')
        except ValueError:
            print("Invalid date. Please try again using YYYY-MM-DD.")


def valid_integer():
    while True:
        user_input = input("Number of guests: ")
        try:
            integer = int(user_input)
            return integer
        except ValueError:
            print("Please enter an integer for number of guests.")


def default_dining_type():
    user_input = input("Do you have a desired seating area?\n"
                       "The names can be found on the venues resy page under the times.\n"
                       "Press ENTER to default to 'Dining Room': ")
    if not user_input:
        user_input = "Dining Room"
    return user_input


def print_progress(max_dots=10):
    """
    Prints dots on the same line progressively up to max_dots,
    then resets and starts again.

    Args:
        max_dots (int): The maximum number of dots before resetting (default is 10).
    """
    if not hasattr(print_progress, "count"):
        print_progress.count = 0

    print_progress.count += 1

    if print_progress.count > max_dots:
        sys.stdout.write('\r' + ' ' * max_dots + '\r')  # Clear the line
        print_progress.count = 1  # Reset to 1

    sys.stdout.write('\r' + '.' * print_progress.count)
    sys.stdout.flush()


def config_parser() -> dict:
    """
    Handles all the config values, including validation of values. Determines if user input is required.
    :return:
    """
    file_path = input("Paste 'configs.toml' file path: ")
    if not file_path:
        file_path = 'configs.toml'
    print(file_path)

    try:
        with open(file_path, 'r') as file:
            data = tomllib.loads(file.read())
    except FileNotFoundError as fnf:
        print("Unable to locate the config file, please try again!")
        print(fnf)
        exit()

    value = False if any(
        data['reservation_details'][item] is False for item in data['reservation_details']) else True

    if value is True:
        party_size = data['reservation_details']['party_size']
        booking_time = data['reservation_details']['military_booking_time']
        booking_date = data['reservation_details']['date']
        venue_url = data['reservation_details']['venue_url']
        desired_seating = data['reservation_details']['desired_seating']

    elif value is False:
        venue_url = input("Please paste the venue page URL from resy.com: ")
        print('\n')
        booking_date = valid_date()
        print('\n')
        party_size = valid_integer()
        print('\n')
        booking_time = input("Please enter the target booking time in military time (HH:MM:SS).\n"
                             "In general these are in 15 min increments: ")
        print('\n')
        desired_seating = default_dining_type()
        print('\n')

    print(f"\n-----Details-----\n"
          f"Date: {booking_date}\n"
          f"Time: {booking_time}\n"
          f"Guests: {party_size}\n"
          f"Desired seating type: {desired_seating}"
          f"\n-----------------\n")

    value_dict = {'party_size': party_size, 'booking_time': booking_time, 'booking_date': booking_date,
                  'venue_url': venue_url, 'desired_seating': desired_seating, 'api_key': data['credentials']['api_key'],
                  'file_path': file_path}
    return value_dict
