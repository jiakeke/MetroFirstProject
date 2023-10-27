# MetroFirstProject

The group project for the first semester of Metropolia

## INSTALL

* Virtual Environment
    ```
    pip install virtualenv
    virtualenv my_env
    source my_env/bin/activate
    ```
    It is recommended to use a `virtualenv` for installation, which is helpful for isolating dependency packages between projects.
    Then you can install the package in a virtual environment dedicated to this project.

* Dependent software packages installation
    ```
    pip install -r requirements.txt
    ```

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


