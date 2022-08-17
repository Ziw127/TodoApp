import os
SECRET_KEY = os.urandom(32)

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://newuser:postgres@localhost:5432/list'