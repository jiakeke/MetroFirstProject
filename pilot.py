"""%(program)s:  Pilot Game Center

usage:  python %(program)s command

Common Commands:

    help          -- print this help text
    play          -- play the game
    initdb        -- database initialization
"""

import mysql.connector
import os
import sys
from geopy.distance import geodesic

program = os.path.basename(sys.argv[0])

db_name = 'pilot'
db_user = ''
db_pass = ''
db_host = 'localhost'

# set the db related variables in config.py
if os.path.exists('config.py'):
    from config import *


def get_database_connection():
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        database=db_name,
        user=db_user,
        password=db_pass,
        autocommit=True
    )
    return connection


def register_user():
    connection = get_database_connection()
    cursor = connection.cursor()

    while True:
        user = input("Enter your desired username: ")
        password = input("Enter your password: ")

        # Check if the username already exists
        cursor.execute("SELECT id FROM user WHERE name = %s", (user,))
        if cursor.fetchone():
            print("This username is already taken. Please choose another one.")
        else:
            # Insert the new user
            cursor.execute("INSERT INTO user (name, password) VALUES (%s, %s)", (user, password))

            # Get the id of the newly registered user
            user_id = cursor.lastrowid

            # Assign the aircraft with id=1 to the user
            cursor.execute("INSERT INTO user_aircrafts (user_id, aircraft_id) VALUES (%s, 1)", (user_id,))

            connection.commit()
            print(f"User {user} registered successfully!")
            break

    cursor.close()
    connection.close()


def login_user():
    connection = get_database_connection()
    cursor = connection.cursor()

    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        cursor.execute("SELECT id FROM user WHERE name = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            print(f"Welcome back, {username}!")
            cursor.close()
            connection.close()
            return user[0]
        else:
            print("Invalid username or password. Please try again.")


def login_or_register():
    """
    The login or registration page is displayed until the login is successful.

    The user needs to enter the username and password. If the username exists,
    the password is verified. If the username and password match, the login is
    successful. If the username does not exist, the user will be automatically
    registered and the login will be successful.

    Return the username after logging in.
    """
    while True:
        choice = input("\nDo you want to [R]egister or [L]ogin? (R/L): ").upper()
        if choice == 'R':
            register_user()
            break
        elif choice == 'L':
            user_id = login_user()
            if user_id:
                return user_id
            break
        else:
            print("Invalid choice. Please choose R for Register or L for Login.")


def menu():
    """
    After logging in, it displays: Main Menu:
    (Menu: 1. Game, 2. Store, 3. Gallery, 4. Ranking, 5. Quit)
    """
    # Show the menu here
    menus = {
        '1': {'name': 'Game', 'method': game_menu},
        '2': {'name': 'Store', 'method': store_menu},
        '3': {'name': 'Gallery', 'method': gallery_menu},
        '4': {'name': 'Ranking', 'method': ranking_menu},
        '5': {'name': 'Quit', 'method': byebye},
    }

    while True:
        number = input(
            "Please choose the number in the menu to enter the corresponding "
            "section."
        )
        if number in menus:
            method = menus[number]['method']
            method()


def get_user_props():
    """
    Returns the maximum range and passenger capacity of all planes owned by the
    player
    """
    pass
    #return (max_range, capacity)


def game_menu():
    """
    Display the game level information, include:
        - Number of people,
        - Departure,
        - Destination,
        - Quotation.

    Display sub menu:
    (Game Menu: 1. Plane1, 2. Plane2, 3. Plane3, ..., R. Refresh, Q. Go Back)
    """
    while True:
        max_range, capacity = get_user_props()
        game_props = game_level_display()

        number = input(
            "Please choose the plane number to "
            "section."
        )
        if number == 'R':
            continue

        elif number == 'Q':
            break

        else:
            # Start game
            game_play(max_range, capacity, *game_props)


def game_level_display(max_range, capacity):
    """
    Display a teaching game for the new user, or a random game.
    """
    pass
    #return (quantity, departure, destination, quotation, weather, temperature)


def game_play(max_range, capacity, quantity, departure, destination, quotation, weather, temperature):
    """
    Play the game, include:
        - Calculate the carbon emission,
        - Calculate the income,
        - Play cutscene,
        - If the task is successful, display a success message and:
            - Save the balance,
            - Save the amount,
            - Save the air-miles,
            - Save the flights,
            - Set new_user_mode to false if previously a new user,

        - If the task fails, show reasons for failure and losses then:
            - Save balance deduction,

        - Go back to the game menu, awaiting for a new task.

    """
    pass

def store_menu():
    """
    Display all the planes on sale, include:
        - An ascii picture,
        - Name,
        - Description,
        - Maximum range
        - Carrying capacity
        - Price,
        - Carbon emission coefficient.

    Display sub menu:
    (Store Menu: Enter the plane number to buy, or press Q. Go Back)
    """
    pass


def gallery_menu():
    """
    Display all user-owned planes, include:
        - An ascii picture,
        - Name,
        - Description,
        - Maximum range
        - Carrying capacity
        - Price,
        - Carbon emission coefficient.

    Display sub menu:
    (Gallery Menu: Press Q. Go Back)
    """
    pass


def ranking_menu():
    """
    Display all user ranking, include:
    Sequence    Username    Balance     Amount      Air-miles   Flights
    1           Gary        32332       32332232    2323 km     32
    2           Anqi        3322        30000       323 km      33
    3           Lucas       2323        10000       322 km      22
    ...         ...         ...         ...         ...         ...

    Display sub menu:
    (Ranking Menu: Press Q. Go Back)
    """
    pass


def byebye():
    """
    Display a goodbye message and end the process.
    """
    pass


def play():
    #Set username as a global variable and do not modify it.
    global username
    username = login_or_register()
    if username:
        menu()
    else:
        byebye()

def run_command(cmd):
    os.system(cmd)

def main():
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd in cmds_map:
        method = cmds_map[cmd]
        method()
    else:
        usage()
        sys.exit(0)

def usage():
    print(__doc__ % {"program": program})


def initdb():
    run_command(f'mysql -u {db_user} -p{db_pass} -e "DROP DATABASE {db_name}"')
    run_command(f'mysql -u {db_user} -p{db_pass} -e "CREATE DATABASE {db_name}"')
    run_command(f'mysql -u {db_user} -p{db_pass} {db_name} < database.sql')
    run_command(f'mysql -u {db_user} -p{db_pass} {db_name} < update.sql')


cmds_map = {
    'help': usage,
    'initdb': initdb,
    'play': play,
}


if __name__ == "__main__":
    main()

