"""
Name: db_connection.py

Module for managing database connection pool using psycopg2.
This module contains singleton class DatabaseConnection which can be used
to create and manage pool of database connections using psycopg2 lib.
The class ensures that only one instance of the connection pool is created.
"""
import psycopg2.pool
import psycopg2


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
    def __init__(self, minconn, maxconn, *args, **kwargs):

        self.minconn = minconn
        self.maxconn = maxconn

        self._args = args
        self._kwargs = kwargs

        self._pool = []
        self._used = {}

        for i in range(self.minconn):
            self._connect()

    def _connect(self):
        conn = psycopg2.connect(*self._args, **self._kwargs)
        self._pool.append(conn)
        return conn

    def get_connection(self):
        if len(self._pool) > 0:
            conn = self._pool.pop()
            self._used[conn] = True
            return conn

        elif len(self._used) < self.maxconn:
            conn = self._connect()
            self._pool.remove(conn)
            self._used[conn] = True
            return conn
        else:
            return "Connection pool exhausted."

    def put_away_connection(self, conn):
        del self._used[conn]
        if len(self._pool) < self.minconn:
            self._pool.append(conn)
        else:
            conn.close()

    def close_all(self):
        for connection in self._pool:
            connection.close()
        for connection in self._used:
            connection.close()
        self._pool = []
        self._used = {}

    # TODO - execute query method.
    def execute_query(self):
        pass

    def print_pool_content(self):
        return f"Pool List: {self._pool}\nLen of Pool: {len(self._pool)}"

    def print_used_content(self):
        return f"Used Dict: {self._used}\nLen of Used: {len(self._used)}"


# class DatabaseConnection(metaclass=DatabaseConnectionMeta):
#     """
#     The DatabaseConnection class used to create and manage a pool of database connections
#     using the psycopg2 library.

#     Attributes:
#         minconn(int): minimum number of connections.
#         maxconn(int): maximum number of connections.
#         host(str):
#         db_user(str): username of postgresql user, which will connect to the db.
#         db_password(str): password for the postgresql user.
#         db_name(str): name of the postgresql database.

#     Methods:
#         __init__ : Initializes the connection pool with given credentials.
#         get_connection() : Returns free connection from the pool.
#         put_away_connection() : Puts away the connection.
#         execute_query() : Execute query during the connection.
#         close_all_connections() : Closing all opened connections.
#     """

#     def __init__(
#         self,
#         minconn: int,
#         maxconn: int,
#         host: str,
#         db_user: str,
#         db_password: str,
#         db_name: str,
#     ):
#         """
#         Creation of a database connection pool.
#         Args:
#             :minconn(int): minimum number of connections.
#             :maxconn(int): maximum number of connections.
#             :host(str):
#             :db_user(str): username of postgresql user, which will connect to the db.
#             :db_password(str): password for the postgresql user.
#             :db_name(str): name of the postgresql database.
#         Returns:
#             None
#         Example:
#              connection1 = DatabaseConnection(1, 10, "localhost", "user", "password", "my_db")
#         """

#         self.pool = psycopg2.pool.SimpleConnectionPool(
#             minconn,
#             maxconn,
#             host=host,
#             user=db_user,
#             password=db_password,
#             database=db_name,
#             port=5431,
#         )

#     def get_connection(self) -> "psycopg2.extensions.connection":
#         """
#         get_connection method returns a free connection from the pool.

#         Returns:
#             psycopg2.extensions.connection(obj): object created from psycopg2.extensions.connection
#             which represents a single connection. It can be used to execute SQL statements,
#             commit and rollback transactions.
#         """
#         return self.pool.getconn()

#     def put_away_connection(self, connection: "psycopg2.extensions.connection") -> None:
#         """_summary_

#         Args:
#             connection (_type_): _description_
#         """
#         self.pool.putconn(connection)

#     def execute_query(self, query: str) -> None:
#         """
#         execute_query method executes sql query through our database connection.
#         Args:
#             query(str): just SQL query.
#         Returns:
#             None
#         Example:
#             connection1.execute_query("SELECT * FROM table1;")
#         """
#         connection = self.get_connection()
#         cursor = connection.cursor()
#         cursor.execute(query)
#         connection.commit()
#         cursor.close()
#         self.put_away_connection(connection)

#     def close_all_connections(self) -> None:
#         """
#         Closing all existing connections.
#         Returns:
#             None
#         """
#         self.pool.closeall()
