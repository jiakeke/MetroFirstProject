

def login_or_register():
    """
    The login or registration page is displayed until the login is successful.

    The user needs to enter the username and password. If the username exists,
    the password is verified. If the username and password match, the login is
    successful. If the username does not exist, the user will be automatically
    registered and the login will be successful.

    Return the username after logging in.
    """
    pass


def menu():
    """
    After logging in, it displays: Main Menu:
    (Menu: 1. Game, 2. Store, 3. Gallery, 4. Ranking, 5. Quit)
    """
    # Show the menu here

    while True:
        number = input(
            "Please choose the number in the menu to enter the corresponding "
            "section."
        )
        match number:
            case "1"
                game_menu()
            case "2"
                store_menu()
            case "3"
                gallery_menu()
            case "4"
                ranking_menu()
            case "5"
                byebye()


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


def main():
    username = login_or_register()
    if username:
        #Set username as a global variable and do not modify it.
        global username
        menu()
    else:
        byebye()


if __name__ == "__main__":
    main()
