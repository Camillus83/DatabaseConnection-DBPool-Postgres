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

    database = DatabaseUtility(
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, DB_CONTAINER_NAME
    )
    database.container_start()
    database.create_tables()

    db_pool_1 = DBConnectionPool(
        2,
        3,
        host="localhost",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=POSTGRES_PORT,
    )
    db_pool_2 = DBConnectionPool(
        1,
        5,
        host="127.0.0.1",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=POSTGRES_PORT,
    )

    log.info("************** START **************")
    log.info("************** CREATING DB_POOL OBJECTS **************")
    log.info("ID of db_pool_1: %s", str(id(db_pool_1)))
    log.info("ID of db_pool_2: %s", str(id(db_pool_2)))
    log.info(
        "ID of db_pool_1 and db_pool_2 are identical? %s",
        str(id(db_pool_1) == id(db_pool_2)),
    )

    log.info(
        "db_pool_1 minconn val: %s, maxconn val: %s",
        str(db_pool_1.minconn),
        str(db_pool_1.maxconn),
    )
    log.info(
        "db_pool_2 minconn val: %s, maxconn val: %s",
        str(db_pool_2.minconn),
        str(db_pool_2.maxconn),
    )

    log.info("**************")
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("**************")
    log.info("Content of DB used dict:")
    log.info(db_pool_2.print_used_content())

    connection1 = db_pool_1.get_connection()
    log.info("************** CONNECTION 1 ************** ")
    log.info("Connection 1: %s", str(connection1))
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("Content of DB used dict:")
    log.info(db_pool_1.print_used_content())

    connection2 = db_pool_1.get_connection()
    log.info("************** CONNECTION 2 ************** ")
    log.info("Connection 2: %s", str(connection2))
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("Content of DB used dict:")
    log.info(db_pool_1.print_used_content())

    connection3 = db_pool_1.get_connection()
    log.info("************** CONNECTION 3 ************** ")
    log.info("Connection 3: %s", str(connection3))
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("Content of DB used dict:")
    log.info(db_pool_1.print_used_content())

    connection4 = db_pool_1.get_connection()
    log.info("************** CONNECTION 4 ************** ")
    log.info("Connection 4: %s", str(connection4))
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("Content of DB used dict:")
    log.info(db_pool_1.print_used_content())

    log.info("************** CONNECTION 3 CLOSE ************** ")
    db_pool_1.return_connection(connection3)
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("Content of DB used dict:")
    log.info(db_pool_1.print_used_content())

    log.info("************** GET ALL RECORDS FROM TABLE 1 ************** ")
    result = db_pool_1.execute_query("SELECT * FROM table1;")
    log.info("Query result: %s", str(result))
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("Content of DB used dict:")
    log.info(db_pool_1.print_used_content())

    log.info("************** CLOSING ALL CONNECTIONS ************** ")
    db_pool_1.close_all()
    log.info("Content of DB pool: ")
    log.info(db_pool_1.print_pool_content())

    log.info("Content of DB used dict:")
    log.info(db_pool_1.print_used_content())

    database.container_stop()
    log.info("************** END **************")


if __name__ == "__main__":
    sys.exit(main())
