import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)


import pytest
from planetly.app import init_app, init_database_connection
from mongoengine import get_connection

TEST_CONFIG = {
    "DB_USER_NAME": "admin",
    "DB_PASSWORD":  "password",
    "DB_URL": "127.0.0.1",
    "HOST": "mongomock"
}


@pytest.fixture
def app():
    app = init_app(TEST_CONFIG)

    yield  app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def tear_downdb():
    def clean_up():
        conn = get_connection("default")
        conn.drop_database("assignment")
    return clean_up

@pytest.fixture
def db(app):
    init_database_connection(app)
