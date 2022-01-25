import os
from os import environ
from dotenv import load_dotenv

path = os.path.join(os.getcwd(), "scripts", "local.env")
load_dotenv(path)
DB_USER_NAME = environ.get('DB_USER_NAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_URL = "127.0.0.1"
HOST= "mongodb"
