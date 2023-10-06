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
import random

program = os.path.basename(sys.argv[0])

db_name = 'pilot'
db_user = ''
db_pass = ''
db_host = 'localhost'

# set the db related variables in config.py
if os.path.exists('config.py'):
    from config import *

user_info = {'username': ''}

def get_database_connection():
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        database=db_name,
        user=db_user,
        password=db_pass,
    )
    return connection


def login_or_register():
    """
    The login or registration page is displayed until the login is successful.

    The user needs to enter the username and password. If the username exists,
    the password is verified. If the username and password match, the login is
    successful. If the username does not exist, the user will be automatically
    registered and the login will be successful.

    Return the username after logging in.
    """
    connection = get_database_connection()
    cursor = connection.cursor()

    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        cursor.execute(f"SELECT password FROM user WHERE name = '{username}'")
        result = cursor.fetchone()

        if result:
            if result[0] == password:
                print(f"Login successful!\nWelcome {username}!")
                cursor.close()
                connection.close()
                user_info['username'] = username
                return username
            else:
                print("Incorrect password. Please try again.")
        else:
            user_choice = input("A non-existent username has been detected. "
                                "Do you want to register?"
                                "(\nEnter yes to register, "
                                "any other to login again):\n")
            if user_choice == "yes":
                try:
                    cursor.execute(
                        "INSERT INTO user (name, password, status) "
                        f"VALUES ('{username}', '{password}', true)")
                    cursor.execute(
                        "INSERT INTO "
                        "user_aircraft (user_id, aircraft_id) "
                        "SELECT id, 1 FROM user "
                        f"WHERE name = '{username}'")
                    print("User registered and login successful!"
                          f"\nWelcome {username}!")
                    connection.commit()
                    cursor.close()
                    connection.close()
                except mysql.connector.Error as err:
                    print(err)
                    connection.rollback()
                print(username)
                user_info['username'] = username
                return username
            else:
                continue


def menu():
    """
    After logging in, it displays: Main Menu:
    (Menu: 1. Game, 2. Store, 3. Gallery, 4. Ranking, 5. Quit)
    """
    # Show the menu here
    menus = {
        '1': {'name': 'Start Game', 'method': game_menu},
        '2': {'name': 'Store', 'method': store_menu},
        '3': {'name': 'Aircraft Gallery', 'method': gallery_menu},
        '4': {'name': 'Ranking', 'method': ranking_menu},
        '5': {'name': 'Quit', 'method': byebye},
    }

    print("--- Main manu ---")
    for key, value in menus.items():
        print(f"{key}. {value['name']}")

    while True:
        number = input(
            "Please choose the number in the menu to enter the corresponding "
            "section:"
        )
        if number in menus:
            method = menus[number]['method']
            method()


def get_user_props():
    """
    Returns the maximum range and passenger capacity of all planes owned by the
    player
    """
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("select passenger_capacity, flight_range "
            "from aircraft, user_aircraft, user "
            "where aircraft.id = aircraft_id "
            f"and user.id = user_id and user.name = '{user_info['username']}'")
    result = cursor.fetchall()
    max_capacity = max([capacity[0] for capacity in result])
    max_range = max([flight_range[1] for flight_range in result])

    cursor.close()
    connection.close()
    return max_range, max_capacity


def get_random_airport_from_db():
    connection = get_database_connection()
    cursor = connection.cursor()

    query = ("SELECT name, latitude_deg, longitude_deg FROM airport "
             "WHERE continent = 'EU' ORDER BY RAND() LIMIT 1")
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    if result:
        return {"name": result[0], "coords": (result[1], result[2])}
    return None


def tutorial():
    start_airport = 'Berlin Tegel Airport'
    end_airport = 'Hamburg Airport'
    distance = 255.96
    passenger = 10
    reward = 1000
    return start_airport, end_airport, distance, passenger, reward

def calculate_carbon_emission(distance):
    """
    Calculate the carbon emission based on the given distance.
    """
    if distance <= 200:
        return distance * 0.275
    elif 200 < distance <= 1000:
        return 55 + 0.105 * (distance - 200)
    else:
        return distance * 0.139


def calculate_distance(start_airport, destination_airport):
    distance = geodesic(start_airport["coords"],
                        destination_airport["coords"]).kilometers
    return distance


def generate_new_task():
    while True:
        start_airport = get_random_airport_from_db()
        destination_airport = get_random_airport_from_db()

        while start_airport["name"] == destination_airport["name"]:
            destination_airport = get_random_airport_from_db()

        distance = round(calculate_distance(start_airport,
                                            destination_airport), 2)
        passenger = random.randint(10, 500)
        max_range, max_capacity = get_user_props()
        if (distance <= max_range * 1.1) and (
                passenger <= max_capacity * 1.1):
            reward = random.randint(int(distance * 10), int(distance * 20))
            new_task = (start_airport["name"], destination_airport["name"],
                        distance, passenger, reward)
            return new_task


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
    print("Goodbye!")
    exit()


def play():
    #Set username as a global variable and do not modify it.
    login_or_register()
    if user_info['username']:
        menu()
    else:
        byebye()

def run_command(cmd):
    os.system(cmd)

def main():
    if len(sys.argv) == 1:
        play()
    cmd = sys.argv[1]
    if cmd in cmds_map:
        method = cmds_map[cmd]
        method()
    else:
        play()

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



