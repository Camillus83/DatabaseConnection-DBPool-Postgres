"""
Name: db_connection.py
Module for managing database connection pool using psycopg2.
"""
import logging
import sys
import threading

import psycopg2


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("database_connection_pool")


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
        kwargs: host, port, db_user, user_pass
        _pool(list): list with available connections.
        _used(dict): dictionary with connections that are currently used by clients.
        lock(obj):

    Methods:
        __init__: creates DBConnectionPool instance.
        get_connection(): returns DB connection from the pool, or creates new when pool is empty.
        return_connection(): closes a single DB connection and store that into pool.
        close_all(): closes all DB connections.
        print_pool_content(): returns a string with _pool content.
        print_used_content(): returns a string with _used content.
    """

    def __init__(self, minconn: int, maxconn: int, **kwargs) -> None:
        """Creation of database connection pool.
            Args:
                :minconn(int): minimum number of connections.
                :maxconn(int): maximum number of connections.
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

        self._kwargs = kwargs

        self._pool = [psycopg2.connect(**self._kwargs) for _ in range(self.minconn)]
        self._used = []

        self.lock = threading.Lock()

        # Creation of the required number of connections, which will be stored in db pool.

        # for _ in range(self.minconn):
        #     conn = psycopg2.connect(**self._kwargs)
        #     self._pool.append(conn)

    def get_connection(self) -> "psycopg2.extensions.connection":
        """Returns a database connection.
        Returns:
            psycopg2.extensions.connection: psycopg2.extensions.connection object.
        """
        with self.lock:
            if (len(self._used) + len(self._pool)) < self.maxconn:
                if self._pool:
                    conn = self._pool.pop()
                else:
                    conn = psycopg2.connect(**self._kwargs)
                self._used.append(conn)
                return conn

            log.warning("too many connections")
            raise Exception("Too many connections.")
            # return None

    def return_connection(self, conn: "psycopg2.extensions.connection") -> None:
        """Closing a database connection."""

        with self.lock:
            self._used.remove(conn)
            self._pool.append(conn)

    def close_all(self) -> None:
        """Closes all existing database connections."""
        with self.lock:
            for connection in self._pool:
                connection.close()
            for connection in self._used:
                connection.close()
            self._pool = []
            self._used = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()

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
        return {
            "available connections (_pool)": len(self._pool),
            "in use connections (_used)": len(self._used),
        }

    def pool_length(self) -> int:
        """Returns pool length"""
        return len(self._pool)

    def used_length(self) -> int:
        """Return used connections length"""
        return len(self._used)
