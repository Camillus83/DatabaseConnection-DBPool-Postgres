"""
Name: db_utils
This module provides class which contains methods for managing a PostgreSQL database.
"""
import time
import subprocess
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("database_utility")

def get_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table1;")
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result

class DatabaseUtility:
    """
    Database utility class.

    Attributes:
        postgres_user(str): username of postgresql user, which will connect to the db.
        postgres_password(str): password for the postgresql user.
        postgres_db(str): name of the postgresql database.
        postgres_port(int):
        db_container_name(str): name of the container which runs postgresql.

    Methods:
        container_start() : starting a postgresql container.
        create_tables() : creating tables in postgresql container database,
                            and inserting data into them.
        drop_tables() : dropping existing tables in postgresql database.
        container_stop() : stops a running postgresql container. Removing
                            that container and associated volumes.
    """

    def __init__(
        self,
        postgres_user: str,
        postgres_password: str,
        postgres_db: str,
        postgres_port: int,
        db_container_name: str,
    ):
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.postgres_db = postgres_db
        self.postgres_port = postgres_port
        self.db_container_name = db_container_name

    def container_start(self) -> None:
        """
        Start a PostgreSQL container using Docker Compose.
        :return: None
        """
        try:
            subprocess.run(["docker-compose", "up", "-d"], check=True)
        except subprocess.CalledProcessError as docker_error:
            log.error("Docker container starting error: %s", str(docker_error))

        time.sleep(2)  # Sleep 2 seconds to wait for server/accepting connections.

        log.info("************** Postgres container is running. **************")

    def create_tables(self) -> None:
        """
        Create sample tables and records in database.
        :return: None
        """

        prefix = [
            "docker",
            "exec",
            "-it",
            self.db_container_name,
            "psql",
            "-U",
            self.postgres_user,
            "-d",
            self.postgres_db,
            "-c",
        ]

        commands = [
            "CREATE TABLE IF NOT EXISTS table1 (id SERIAL PRIMARY KEY, name VARCHAR);",
            "CREATE TABLE IF NOT EXISTS table2 (id SERIAL PRIMARY KEY, name VARCHAR);",
            "INSERT INTO table1 (name) VALUES ('Kamil') ON CONFLICT DO NOTHING;",
            "INSERT INTO table1 (name) VALUES ('Majlo') ON CONFLICT DO NOTHING;",
            "INSERT INTO table2 (name) VALUES ('John') ON CONFLICT DO NOTHING;",
            "INSERT INTO table2 (name) VALUES ('Johnny') ON CONFLICT DO NOTHING;",
        ]

        for command in commands:
            command_to_execute = prefix + [command]
            try:
                subprocess.run(
                    command_to_execute,
                    check=True,
                )

            except subprocess.CalledProcessError as err:
                log.error("Create table error: %s", str(err))

    # TODO - fix that drop_tables method.
    def drop_tables(self) -> None:
        """
        Dropping existing tables in database.
        :return: None
        """
        try:
            subprocess.run(
                [
                    "docker",
                    "exec",
                    "-it",
                    self.db_container_name,
                    "psql",
                    "-U",
                    self.postgres_user,
                    "-d",
                    self.postgres_db,
                    "DROP TABLE IF EXISTS table1, table2;",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as err:
            log.error("Drop tables error: %s", str(err))

    def container_stop(self) -> None:
        """
        Stop and remove a Docker container.
        :return: None
        """
        try:
            subprocess.run(["docker", "stop", self.db_container_name], check=True)
            subprocess.run(["docker", "rm", self.db_container_name], check=True)
            subprocess.run(
                ["docker", "volume", "rm", "task3expertsoftserve_db_data"], check=True
            )
        except subprocess.CalledProcessError as err:
            log.error("Container stop error: %s", str(err))
