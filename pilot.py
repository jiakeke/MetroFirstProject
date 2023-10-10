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

from flying import flying, clear_screen
from tabulate import tabulate

program = os.path.basename(sys.argv[0])

game_name = """
=============================================
 _____
|  ___|
| |__ _   _ _ __ ___  _ __   ___  __ _ _ __
|  __| | | | '__/ _ \| '_ \ / _ \/ _` | '_ \\
| |__| |_| | | | (_) | |_) |  __/ (_| | | | |
\____/\__,_|_|  \___/| .__/ \___|\__,_|_| |_|
                     | |
                     |_|
  ___  _      _ _
 / _ \(_)    | (_)
/ /_\ \_ _ __| |_ _ __   ___
|  _  | | '__| | | '_ \ / _ \\
| | | | | |  | | | | | |  __/
\_| |_/_|_|  |_|_|_| |_|\___|


 _____
|_   _|
  | |_   _  ___ ___   ___  _ __
  | | | | |/ __/ _ \ / _ \| '_ \\
  | | |_| | (_| (_) | (_) | | | |
  \_/\__, |\___\___/ \___/|_| |_|
      __/ |
     |___/
=============================================
"""

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
        print('======== Login OR Register ========')
        print()
        username = input("Username: ")
        password = input("Password: ")

        cursor.execute(f"SELECT password FROM user WHERE name = '{username}'")
        result = cursor.fetchone()

        if result:
            if result[0] == password:
                clear_screen()
                print()
                print('======== European Airline Tycoon ========')
                print()
                print(f"Login successful!\n\nWelcome {username}!\n")
                print()
                cursor.close()
                connection.close()
                user_info['username'] = username
                return username
            else:
                print("Incorrect password. Please try again.")
        else:
            user_choice = input("Username Not Found. "
                                "Do you want to register?"
                                "(\nEnter yes to register, "
                                "any other to login again):\n")
            if user_choice == "yes":
                try:
                    cursor.execute(
                        "INSERT INTO user (name, password, status, "
                        "total_amount, balance, carbon_emission) "
                        f"VALUES ('{username}', '{password}', true, 0, 0, 0)")
                    cursor.execute(
                        "INSERT INTO user_aircraft (user_id, aircraft_id) "
                        "SELECT user.id, aircraft.id "
                        "FROM user, aircraft "
                        f"WHERE user.name = '{username}' "
                        "AND plane_key = 'sky_hawk_100';")
                    clear_screen()
                    print()
                    print('======== European Airline Tycoon ========')
                    print()
                    print("User registered and login successful!"
                          f"\n\nWelcome {username}!")
                    print()
                    print()
                    connection.commit()
                    cursor.close()
                    connection.close()
                except mysql.connector.Error as err:
                    print(err)
                    connection.rollback()
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
        '5': {'name': 'Quit', 'method': goodbye},
    }

    while True:
        print("--- Main manu ---")
        for key, value in menus.items():
            print(f"{key}. {value['name']}")
        number = input(
            "Please choose the number in the menu to enter the corresFponding "
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


def get_random_airport():
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
    latitude = "tutorial"
    return start_airport, end_airport, distance, passenger, reward, latitude


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
    """
        Display a teaching game for the new user, or a random game.
    """
    while True:
        start_airport = get_random_airport()
        destination_airport = get_random_airport()

        while start_airport["name"] == destination_airport["name"]:
            destination_airport = get_random_airport()

        distance = round(calculate_distance(start_airport,
                                            destination_airport), 2)
        max_range, max_capacity = get_user_props()
        passenger = random.randint(1, max_capacity + 10)
        emission = calculate_carbon_emission(distance)
        carbon_cost = emission * 1.3
        fuel_cost = distance * 2.5
        total_cost = fuel_cost + carbon_cost
        reward = (int(total_cost) + 500) * random.randint(90, 120) / 100
        new_task = (start_airport["name"], destination_airport["name"],
                    distance, passenger, reward,
                    destination_airport["coords"][0])

        return new_task


def get_weather_index(latitude):
    weather_setting = {
        1: ('Normal', 1.0),
        2: ('Great Weather', 0.9),
        3: ('Heavy Rain', 1.1),
        4: ('Blizzard', 1.3),
        5: ('Snow', 1.2),
        6: ('Thunderstorm', 1.2)
    }
    if latitude == "tutorial":
        return weather_setting[1]
    weather_index = weather_setting[1]
    if random.random() <= 0.20:
        weather_index = weather_setting[2]
    elif random.random() >= 0.80:
        weather_index = weather_setting[3]
    elif latitude >= 60 and random.random() <= 0.05:
        weather_index = weather_setting[4]
    elif latitude >= 40 and random.random() <= 0.10:
        weather_index = weather_setting[5]
    elif latitude <= 30 and random.random() <= 0.15:
        weather_index = weather_setting[6]
    return weather_index


def get_user_aircraft(username):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = ("SELECT aircraft.id, aircraft.name, aircraft.flight_range, "
             "aircraft.passenger_capacity as capacity "
             "FROM user_aircraft JOIN aircraft "
             "ON user_aircraft.aircraft_id = aircraft.id "
             "JOIN user ON user_aircraft.user_id = user.id "
             f"WHERE user.name = '{username}'")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


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

        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT status FROM user WHERE name = '{user_info['username']}'")
        result = cursor.fetchone()
        if result[0] == 1:
            game_props = tutorial()
            cursor.execute(
                "UPDATE user SET status = False "
                f"WHERE name = '{user_info['username']}'")
            connection.commit()
        else:
            game_props = generate_new_task()

        print(f"Fly from {game_props[0]} to {game_props[1]}. "
              f"\nDistance: {game_props[2]} km "
              f"\nCarry {game_props[3]} passengers "
              f"for an offer of {game_props[4]} coins")
        print("Tip: Destination weather may affect flight costs.")
        user_aircraft = get_user_aircraft(user_info['username'])
        for idx, aircraft in enumerate(user_aircraft, 1):
            print(
                f"{idx}. {aircraft[1]} "
                f"- Range: {aircraft[2]}km "
                f"- Capacity: {aircraft[3]} passengers")

        number = input(
            "Please choose the plane number to complete the task"
            "\nR to refresh a new task"
            "\nQ to quit to menu\n"
        )
        if number.isdigit() and 0 < int(number) <= len(user_aircraft):
            selected_aircraft_id = user_aircraft[int(number) - 1][0]
            # Start game
            game_play(
                selected_aircraft_id, max_range, capacity, *game_props[2:])

        elif number == 'R':
            continue

        elif number == 'Q':
            break

        else:
            print("Invalid choice. Please try again.")


def game_play(number, max_range, capacity, distance,
              passenger, reward, latitude):
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

    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT aircraft.carbon_emission FROM aircraft, user_aircraft, user "
        "WHERE user_aircraft.aircraft_id = aircraft.id "
        "AND user_aircraft.user_id = user.id "
        f"AND user_aircraft.id = {number}")
    result = cursor.fetchone()
    carbon_coefficient = result[0]

    carbon_emission = calculate_carbon_emission(distance)
    carbon_cost = carbon_emission * carbon_coefficient
    fuel_cost = distance * 2.2
    weather_index = get_weather_index(latitude)
    total_cost = (fuel_cost + carbon_cost) * weather_index[1]
    cursor.execute(
        "UPDATE user "
        f"SET carbon_emission = carbon_emission + {carbon_emission} "
        f"WHERE name = '{user_info['username']}'")

    refuel_cost = 0
    refuel_times = 0
    if distance > max_range:
        refuel_times = int(distance / max_range)
        refuel_cost = 50 * refuel_times
        total_cost += refuel_cost

    if passenger > capacity:
        print(
            "Task failed! "
            "The number of passengers exceeds your plane's capacity.\n")
        return False

    total_income = round(reward - total_cost, 1)
    if total_income > 0:
        try:
            cursor.execute(f"UPDATE user SET balance = balance + {total_income} "
                           f"WHERE name = '{user_info['username']}'")
            cursor.execute(
                f"UPDATE user SET total_amount = total_amount + {total_income} "
                f"WHERE name = '{user_info['username']}'")
            connection.commit()
        except mysql.connector.Error as err:
                print(err)
                connection.rollback()
    else:
        print(
            "Task failed! "
            "Your cost is larger than profit.\n")
    cursor.execute("SELECT image from aircraft, user_aircraft, user "
                   "WHERE user_aircraft.aircraft_id = aircraft.id "
                   "AND user_aircraft.user_id = user.id "
                   f"AND user_aircraft.id = {number}")
    result = cursor.fetchone()
    flying(result[0])
    cursor.close()
    connection.close()

    if refuel_cost:
        print(
            f"You had to refuel {refuel_times} times during your trip. "
            f"This cost an additional {refuel_cost} coins.")

    print(f"You encountered {weather_index[0]} weather "
          "at your destination airport")
    print(
        f"Task successful!\nYou earned: {total_income}\n"
        f"Total cost was: {total_cost}\n")
    return True


def get_user_balance(cursor):
    username = user_info['username']
    sql = f"SELECT balance FROM user WHERE name = '{username}' LIMIT 1"
    cursor.execute(sql)
    return cursor.fetchone()[0]


def get_planes_table(cursor):
    cursor.execute("SELECT * FROM aircraft")
    headers = cursor.column_names[1: -2]
    headers = ['Number'] + [item.replace('_', ' ').title() for item in headers]
    planes = cursor.fetchall()
    result = [[num] + list(item[1: -2])
                for num, item in enumerate(planes, 1)]
    plane_table = tabulate(result, headers, tablefmt="grid")
    return plane_table, planes


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
    username = user_info['username']
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT id FROM user WHERE name = '{username}'")
    user_id = cursor.fetchone()[0]

    plane_table, planes = get_planes_table(cursor)

    while True:
        print(plane_table)
        _balance = get_user_balance(cursor)
        print(f"Current balance: {_balance}")

        cursor.execute("SELECT aircraft_id FROM user_aircraft"
                      f" WHERE user_id='{user_id}'")
        user_plane_ids = [item[0] for item in cursor.fetchall()]

        shop_menu_choice = input(
            "For checking aircraft image and purchasing, please enter the "
            "number of the aircraft.\n"
            "For going back to the main menu, please press enter.")

        if not shop_menu_choice:
            break

        if not shop_menu_choice.isdigit():
            print("Invalid input, please enter 1 to {len(planes)}.")
            continue

        choice_num = int(shop_menu_choice)
        if choice_num <= 0 or choice_num > len(planes):
            print(f"Invalid input, please enter 1 to {len(planes)}.")
            continue

        _plane = planes[choice_num - 1]
        _image = _plane[-2]
        print(_image)

        _choice = input("Buy(B) or Go back(Others)\n")
        if _choice.lower() != 'b':
            continue

        aircraft_id = _plane[0]
        if aircraft_id in user_plane_ids:
            print("You already have this plane.")
            continue

        _price = float(_plane[4])
        if _balance < _price:
            print("You do not have enough balance.")
            continue

        new_balance = _balance - _price
        try:
            cursor.execute(
                "UPDATE user"
                f" SET balance = {new_balance} "
                f"WHERE id={user_id}")

            cursor.execute(
                "INSERT INTO user_aircraft (user_id, aircraft_id) "
                f"VALUES ({user_id}, {aircraft_id})")
            connection.commit()
        except mysql.connector.Error as err:
            print(err)
            connection.rollback()

        print("Congratulations, you have bought a new plane！")


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


def goodbye():
    """
    Display a goodbye message and end the process.
    """
    print("Goodbye!")
    exit()


def play():
    #Set username as a global variable and do not modify it.
    clear_screen()
    print(game_name)
    login_or_register()
    if user_info['username']:
        menu()
    else:
        goodbye()


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



