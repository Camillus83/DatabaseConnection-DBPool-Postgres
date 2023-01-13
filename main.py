"""_summary_
"""
import os
import sys
import logging
from dotenv import load_dotenv
from db_utils import DatabaseUtility
from db_connection import DatabaseConnection

load_dotenv()
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
DB_CONTAINER_NAME = os.environ["DB_CONTAINER_NAME"]


def main():
    """Main function"""
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    log = logging.getLogger("db_connection_pool_app")

    db = DatabaseUtility(
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, DB_CONTAINER_NAME
    )
    db.container_start()
    db.create_tables()

    connection1 = DatabaseConnection(
        1, 10, "localhost", POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
    )
    connection2 = DatabaseConnection(
        1, 10, "localhost", POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
    )

    log.info("ID of connection1: %s", str(id(connection1)))
    log.info("ID of connection2 %s", str(id(connection2)))

    connection1.execute_query("SELECT * FROM table1;")
    connection2.execute_query("SELECT * FROM table2;")

    # db.drop_tables()
    db.container_stop()
    log.info("END")


if __name__ == "__main__":
    sys.exit(main())
