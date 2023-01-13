"""
Name: db_utility


Description:
This module provides utility functions for managing a PostgreSQL database.
It contains functions for starting PostgreSQL container, initializing the database,
deleting existing database or stoping container.

Functions:
- 'db_container_start()': starts a PostgreSQL container using Docker Compose file.
- 'create_tables()': initializes the database and creates necessary tables.
- 'db_container_stop()': stops a running PostgreSQL container.
"""
import subprocess

# from dotenv import load_dotenv

# load_dotenv()
# POSTGRES_USER = os.environ["POSTGRES_USER"]
# POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
# POSTGRES_DB = os.environ["POSTGRES_DB"]
# POSTGRES_PORT = os.environ["POSTGRES_PORT"]
# DB_CONTAINER_NAME = os.environ["DB_CONTAINER_NAME"]


def db_container_start():
    """
    Start a PostgreSQL container using Docker Compose.
    :return: None
    """
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
    except subprocess.CalledProcessError as docker_error:
        print(
            "Docker container starting error: " + docker_error
        )  # It should go also into logs.


def create_tables(
    db_container_name: str,
    db_user: str,
    db_name: str,
) -> None:
    """
    Initialize 3 tables in the specified container by running specified commands.
    :param db_container_name: the name of the container running the Postgresql database.
    :param db_user: The user to be used to connect to the postgresql database.
    :param db_name: the name of the database to be initialized.
    :return: None
    """

    commands = [
        "CREATE TABLE table1 (id SERIAL PRIMARY KEY, name VARCHAR);",
        "CREATE TABLE table2 (id SERIAL PRIMARY KEY, name VARCHAR);",
        "CREATE TABLE table3 (id SERIAL PRIMARY KEY, age INTEGER);",
    ]

    try:
        for command in commands:
            subprocess.run(
                [
                    "docker",
                    "exec",
                    "-it",
                    db_container_name,
                    "psql",
                    "-U",
                    db_user,
                    "-d",
                    db_name,
                    command,
                ],
                check=True,
            )

    except subprocess.CalledProcessError as docker_error:
        print(
            "Database creation error: " + docker_error
        )  # It should go also into logs.


def db_container_stop(db_container_name: str) -> None:
    """
    Stop and remove a Docker container.
    :param db_container_name: the name of the container to be stopped and removed
    :return: None
    """
    try:
        subprocess.run(["docker", "stop", db_container_name], check=True)
        subprocess.run(["docker", "rm", db_container_name], check=True)
    except subprocess.CalledProcessError as docker_error:
        print(
            "Docker container starting error: " + docker_error
        )  # It should go also into logs.
