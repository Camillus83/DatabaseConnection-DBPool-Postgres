"""Fixtures for pytest tests."""
import os

import pytest
from dotenv import load_dotenv

from db_utils import DatabaseUtility
from db_connection import DBConnectionPool

load_dotenv()
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
DB_CONTAINER_NAME = os.environ["DB_CONTAINER_NAME"]

MIN_CONNECTIONS = 5
MAX_CONNECTIONS = 10


@pytest.fixture(scope="session")
def db_container():
    """
    Prepare and runs a container with postgresql database.
    """
    database = DatabaseUtility(
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, int(POSTGRES_PORT), DB_CONTAINER_NAME
    )
    database.container_start()
    yield database
    database.container_stop()


@pytest.fixture(scope="session")
def db_pool():
    """
    Preparing and returning DBConnectionPool object.
    """
    database_pool = DBConnectionPool(
        MIN_CONNECTIONS,
        MAX_CONNECTIONS,
        host="localhost",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=POSTGRES_PORT,
    )
    yield database_pool
    database_pool.close_all()


@pytest.fixture(scope="session")
def db_pool_2():
    """
    Preparing and returning DBConnectionPool object.
    """
    database_pool = DBConnectionPool(
        15,
        30,
        host="localhost",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=POSTGRES_PORT,
    )
    yield database_pool
    database_pool.close_all()
