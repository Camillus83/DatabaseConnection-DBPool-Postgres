"""
Name: db_connection.py

Module for managing database connection pool using psycopg2.
This module contains singleton class DatabaseConnection which can be used
to create and manage pool of database connections using psycopg2 lib.
The class ensures that only one instance of the connection pool is created.
"""
import logging
import sys
from typing import List, Union
import threading
import psycopg2


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("database_connection_pool")
# TODO - Create some exceptions


class DBConnectionPoolMeta(type):
    """
    The Singleton meta class for DatabaseConnection class.
    This meta class ensures that only one instance of the connection pool is created,
    regardless of how many times the class is instantiated.

    Args:
        _instances(dict): A dictionary to store singletion instances.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DBConnectionPool(metaclass=DBConnectionPoolMeta):
    """The DatabaseConnectionPool class used to create and manage a pool of database connections
    with using the psycopg2 library.

    Attributes:
        minconn(int): minimum number of connections in pool.
        maxconn(int): maximum number of connections in pool.
        args, kwargs: host, port, db_user, user_pass
        _pool(list): list with available connections.
        _used(dict): dictionary with connections that are currently used by clients.
        lock(obj): #TODO add it.

    Methods:
        __init__: creates DBConnectionPool instance.
        _connect(): creates DB connection and store that in _pool.
        get_connection(): returns DB connection from the pool, or creates new when pool is empty.
        return_connection(): closes a single DB connection and store that into pool.
        close_all(): closes all DB connections.
        print_pool_content(): returns a string with _pool content.
        print_used_content(): returns a string with _used content.
    """

    def __init__(self, minconn: int, maxconn: int, *args, **kwargs) -> None:
        """Creation of database connection pool.
            Args:
                :minconn(int): minimum number of connections.
                :maxconn(int): maximum number of connections.
            Returns:
                None
            Example:
               db_pool_1 = DBConnectionPool(
                    5,
                    10,
                    host="localhost",
                    user="postgres_usr",
                    password="postgres_pass",
                    dbname="postgres_db",
                    port=5431,
        )
        """
        self.minconn = minconn
        self.maxconn = maxconn

        self._args = args
        self._kwargs = kwargs

        self._pool = []
        self._used = []

        self.lock = threading.Lock()

        # Creation of the required number of connections, which will be stored in db pool.
        for _ in range(self.minconn):
            self._connect()

    def _connect(self):
        """Create the connection to the database, then store that in the _pool list.
        Arguments:
            None
        Returns:
            :obj: - psycopg2 connection object.
        """
        conn = psycopg2.connect(*self._args, **self._kwargs)
        self._pool.append(conn)
        return conn

    # Two different types of variable returned
    def get_connection(self) -> Union[psycopg2.extensions.connection, str]:
        """Returns a database connection.
        Arguments:
            None
        Returns:
            psycopg2.extensions.connection: object created from psycopg2.extensions.connection
            which represents a single connection. It can be used to execute SQL statements,
            commit and rollback transactions.
        """
        with self.lock:
            if len(self._pool) > 0:
                conn = self._pool.pop()
                self._used.append(conn)
                return conn  # returning psycopg2 obj.

            elif len(self._used) < self.maxconn:
                conn = self._connect()
                self._pool.remove(conn)
                self._used.append(conn)
                return conn  # returning psycopg2 obj.

            else:
                return "Connection pool exhausted."  # returning string.

    def return_connection(self, conn: "psycopg2.extensions.connection") -> None:
        """Closing a database connection.
        Arguments:
            None
        Returns:
            None
        """
        with self.lock:
            self._used.remove(conn)
            if len(self._pool) < self.minconn:
                self._pool.append(conn)
            else:
                conn.close()

    def close_all(self) -> None:
        """Closes all existing database connections."""
        with self.lock:
            for connection in self._pool:
                connection.close()
            for connection in self._used:
                connection.close()
            self._pool = []
            self._used = []

    def execute_query(self, query: str) -> List:
        """Executes SQL query in database.
        Args:
            query (str): SQL query
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
            else:
                result = None
            connection.commit()
            cursor.close()
            self.return_connection(connection)
            return result

        except psycopg2.Error as err:
            log.error("Execute query error: %s", err)
            return None

    def print_pool_content(self) -> str:
        """Returns a string with the content of the _pool variable for logging purposes.
        Returns:
            str: Content of _pool variable
        """
        return f"Pool List: {self._pool}\nLen of Pool: {len(self._pool)}"

    def print_used_content(self) -> str:
        """Returns a string with the content of the _used variable for logging purposes.
        Returns:
            str: Content of _used variable
        """
        return f"Used List: {self._used}\nLen of Used: {len(self._used)}"

    def check_status(self) -> dict:
        """Returns a dict with informations about available connections and in use connections
        Returns:
            dict: info about available and in use connections
        """
        return {"available": len(self._pool), "in use": len(self._used)}
