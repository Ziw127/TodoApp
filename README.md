# SAMPLE VERSION OF TODO APP
This app is written in Python with Flask and SQLAlchemy.

## A. Dependency
In order to run this app, the following dependencies must have been already installed:
1. Postgres. 
 * Start manually: `pg_ctl -D /usr/local/var/postgres start`
 * Stop manually: `pg_ctl -D /usr/local/var/postgres stop -s -m fast`
 
2. Flask.
    A lightweight backend microservices framework. Flask is required to handle requests and responses.
3. FLASK-CORS
    An extension we'll use to handle origin requests from our frontend server
4. jose JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding
   and verifying JWTS.

## B. Database 
The database relations `todos(id, description, complete, list_id)` and `todolists(id, name)` must have been already created in Postgres. We have assumed that the Postgres is running on default port 5432.

* `dropdb todoapp -p 5432 && createdb todoapp -p 5432` 
* Open the database prompt - `psql -p 5432`
* Connect to the database - `\c todoapp` 
* Displays the tables in the database `\dt` 
* Displays the schema of the 'todos' table `\d todos` 
* Displays the schema of the 'todolists' table `\d todolists` 

You can insert a few rows in both the tables. Insert first in the `todolists` relation. 


## C. Steps to Run the App: 
* `python3 -m venv env` set the virtual environment for Pyhton 
* `source env/bin/activate` activate the venv
* `python -m pip install -r requirements.txt` to install dependencies. For Mac users, if you face difficulty in installing the `psycopg2`, you may consider intalling the `sudo brew install libpq` before running the `requirement.txt`. 
* `python3 app.py` to run the app (http://127.0.0.1:5000/ or http://localhost:5000)
* `deactivate` de-activate the virtual environment
* To run the server, execute:

    $export FLASK_APP=flaskr
    $export FLASK_ENV=development
    $flask run

    Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.
    Setting the FLASK_APP variable to app.py directs flask to use the app.py file to find the application.

