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

import flying
from tabulate import tabulate




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
                        "INSERT INTO user (name, password, status, "
                        "total_amount, balance, carbon_emission) "
                        f"VALUES ('{username}', '{password}', true, 0, 0, 0)")
                    cursor.execute(
                        "INSERT INTO user_aircraft (user_id, aircraft_id) "
                        "SELECT user.id, aircraft.id "
                        "FROM user, aircraft "
                        f"WHERE user.name = '{username}' "
                        "AND plane_key = 'sky_hawk_100';")
                    print("User registered and login successful!"
                          f"\nWelcome {username}!")
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
        '5': {'name': 'Quit', 'method': byebye},
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
        reward = (total_cost + 500) * random.randint(90, 120) / 100
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
            return game_menu()



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
    fuel_cost = distance * 2.5
    total_cost = (fuel_cost + carbon_cost) * get_weather_index(latitude)[1]
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
        return game_menu()

    total_income = reward - total_cost
    cursor.execute(f"UPDATE user SET balance = balance + {total_income} "
                   f"WHERE name = '{user_info['username']}'")
    cursor.execute(
        f"UPDATE user SET total_amount = total_amount + {total_income} "
        f"WHERE name = '{user_info['username']}'")
    cursor.close()
    connection.close()
    flying.flying()

    if refuel_cost:
        print(
            f"You had to refuel {refuel_times} times during your trip. "
            f"This cost an additional {refuel_cost} coins.")

    print(
        f"Task successful!\nYou earned: {total_income}\n"
        f"Total cost was: {total_cost}\n")
    game_menu()

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
    connection = get_database_connection()
    while True:
        def store_main_interface():
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name, passenger_capacity, "
                "flight_range, price, carbon_emission FROM aircraft"
            )
            result = cursor.fetchall()
            headers = ["id", "name", "passenger capacity", "flight range", "price", "carbon emission"]
            table = tabulate(result, headers, tablefmt="grid")
            print(table)

        store_main_interface()
        shop_menu_choice = input("For checking aircraft image and purchasing, please enter the aircraft's id.\n"
                                 "For going back to the main menu, please press enter. ")
        if not shop_menu_choice:
            break
        try:
            aircraft_id = int(shop_menu_choice)
            if aircraft_id > 0 and aircraft_id < 10:
                cursor = connection.cursor()
                cursor.execute("SELECT image FROM  aircraft WHERE id = %s", (aircraft_id,))
                aircraft_image = cursor.fetchone()
                for item in aircraft_image:
                    print(item)
                aircraft_action = input("1. purchase\n"
                                        "2. Go back to store menu\n")
                try:
                    aircraft_choice = int(aircraft_action)
                    if aircraft_choice == 1:
                        cursor.execute("SELECT aircraft_id, user_id FROM user_aircraft"
                                       " JOIN user ON user.id = user_aircraft.user_id"
                                       f" WHERE name = '{username}'"
                                       f" AND aircraft_id = {aircraft_id}")
                        result = cursor.fetchone()
                        aircraft_repository = None
                        if result is not None:
                            aircraft_repository = result[0]
                            user_id = result[1]
                            print("You already have this plane.")
                        else:

                            cursor.execute("SELECT price FROM aircraft"
                                           f" WHERE id = {aircraft_id}")
                            aircraft_price = float(cursor.fetchone()[0])
                            if aircraft_price:
                                cursor.execute("SELECT balance FROM user"
                                               f" WHERE name = '{username}'")
                                user_balance = float(cursor.fetchone()[0])
                                if user_balance >= aircraft_price:
                                    new_balance = user_balance - aircraft_price
                                    cursor.execute("UPDATE user"
                                                   f" SET balance = {new_balance} "
                                                   f"WHERE name = '{username}'")
                                    cursor.execute(f"SELECT id FROM user WHERE name = '{username}'")
                                    user_id = cursor.fetchone()[0]
                                    cursor.execute("INSERT INTO user_aircraft (user_id, aircraft_id) "
                                                   f"VALUES ({user_id}, {aircraft_id})")
                                    print("Congratulations, you have bought a new plane！")
                                else:
                                    print("You do not have enough balance.")
                            else:
                                print("Aircraft not found.")
                    elif aircraft_choice == 2:
                        continue
                    else:
                        print("Invalid input, please enter 1 or 2.")
                except ValueError:
                    print("Invalid input, please enter 1 or 2.")
            else:
                print("Aircraft not found.")
        except ValueError:
            print("Invalid input, please enter 1 to 9.")






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



