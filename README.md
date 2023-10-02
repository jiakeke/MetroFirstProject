# MetroFirstProject
The group project for the first semester of Metropolia

## INSTALL

* Rename `config.py.example` to `config.py`, set db_user, db_pass inside it to overwrite the variables in pilot.py.
    ```
    db_user = 'your_db_username'
    db_pass = 'your_db_password'
    ```

* Initialize database first:
    ```
    python pilot.py initdb
    ```

* Run the game by:
    ```
    python pilot.py play
    ```
