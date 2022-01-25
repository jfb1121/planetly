import os
from os import environ
from dotenv import load_dotenv

path = os.path.join(os.getcwd(), "planetly", "docker.env")
load_dotenv(path)
HOST = environ.get('HOST')
DB_USER_NAME = environ.get('DB_USER_NAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_URL = environ.get('DB_URL') if environ.get('STAGE') == "prod-docker" else \
    "127.0.0.1" # just to make it possible to test outside the container. 
