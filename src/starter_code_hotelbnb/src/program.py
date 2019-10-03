from colorama import Fore
import program_guests
import program_hosts

import data.mongo_setup as mongo_setup

def main():
    # TODO: Setup mongoengine global values
    mongo_setup.global_init()

    print_header()

    try:
        while True:
            if find_user_intent() == 'book':
                program_guests.run()
            else:
                program_hosts.run()
    except KeyboardInterrupt:
        return


def print_header():
    hotel = \
        """
            WELCOME TO HOTEL HOLIDAY INN, DELHI
        """

    print(Fore.WHITE + '****************  Hotel Holiday Inn  ****************')
    print(Fore.GREEN + hotel)
    print(Fore.WHITE + '*********************************************')
    print()
    print("Welcome to Hotel Holiday Inn!")
    print("Why are you here?")
    print()


def find_user_intent():
    print("[g] Book a room ")
    print("[h] Offer extra room space")
    print()
    choice = input("Are you a [g]uest or [h]ost? ")
    if choice == 'h':
        return 'offer'

    return 'book'


if __name__ == '__main__':
    main()