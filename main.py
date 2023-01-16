"""_summary_
"""
import os
import sys
import logging
from dotenv import load_dotenv
from db_utils import DatabaseUtility
from db_connection import DBConnectionPool

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

    connection1 = DBConnectionPool(
        2,
        3,
        host="localhost",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=5431,
    )
    connection2 = DBConnectionPool(
        3,
        10,
        host="localhost",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=5431,
    )
    connection3 = DBConnectionPool(
        3,
        10,
        host="localhost",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=5431,
    )

    print("after creating pool")
    connection1.print_pool()
    connection2.print_used()

    a = connection1.get_connection()
    print("a: ")
    print(a)

    connection1.print_pool()
    connection2.print_used()

    b = connection1.get_connection()
    print("b: ")
    print(b)

    connection1.print_pool()
    connection2.print_used()

    c = connection1.get_connection()
    print("c: ")
    print(c)

    connection1.print_pool()
    connection2.print_used()

    log.info("ID of connection1: %s", str(id(connection1)))
    log.info("ID of connection2 %s", str(id(connection2)))

    log.info("Amount of minConn: %s", str(connection1.minconn))
    log.info("Amount of minConn: %s", str(connection2.minconn))

    # connection1.execute_query("SELECT * FROM table1;")
    # connection2.execute_query("SELECT * FROM table2;")

    # db.drop_tables()
    db.container_stop()
    log.info("END")


if __name__ == "__main__":
    sys.exit(main())
