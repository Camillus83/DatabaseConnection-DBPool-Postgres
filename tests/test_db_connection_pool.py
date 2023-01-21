"""Tests for database connection pool app."""
import pytest

from psycopg2.extensions import connection

from fixtures import db_container, db_pool, db_pool_2, MAX_CONNECTIONS, MIN_CONNECTIONS
from database.db_exceptions import DBConnectionPoolError


def test_singleton(db_container, db_pool, db_pool_2):
    """
    This test function checks that the `db_pool` and `db_pool_2` objects are the same instance.
    """
    assert db_pool is db_pool_2


def test_min_max_connections(db_pool):
    """
    This test function checks that attributes od DBConnectionPool class has correct values.
    """
    assert db_pool.minconn == MIN_CONNECTIONS
    assert db_pool.maxconn == MAX_CONNECTIONS


def test_lists_creation(db_pool):
    """
    This test function checks that if lists for connections in pool list and used list are created
    correctly.
    """
    assert db_pool.pool_length() == MIN_CONNECTIONS
    assert db_pool.used_length() == 0


def test_get_connection(db_pool):
    """
    This test function checks if get_connections function returns a psycopg2 connection object.
    """
    conn = db_pool.get_connection()
    assert conn is not None
    assert isinstance(conn, connection)
    db_pool.return_connection(conn)

def test_put_foreign_connection(db_pool):
    """
    This test functions checks if  raising exception works when someone tries to return
    foreign connection.
    """
    with pytest.raises(DBConnectionPoolError, match="That is not our connection!"):
        conn = {"fake":"connection"}
        db_pool.return_connection(conn)


def test_put_connection(db_pool):
    """
    This test functions checks if returning connection back to the pool works correctly.
    """
    pool_len_before_conn = db_pool.pool_length()
    used_len_before_conn = db_pool.used_length()
    conn = db_pool.get_connection()
    assert db_pool.used_length() == used_len_before_conn + 1
    db_pool.return_connection(conn)
    assert db_pool.pool_length() == pool_len_before_conn


def test_connections_exhausted(db_pool):
    """
    This test function checks if raising exception works when it's too many connections.
    """
    with pytest.raises(DBConnectionPoolError, match="Too many connections."):
        for _ in range(MAX_CONNECTIONS + 1):
            db_pool.get_connection()
    db_pool.close_all()


def test_closing_all_connections(db_pool):
    """
    This test function checks if closing all connections method works correctly.
    """
    for _ in range(MIN_CONNECTIONS + 1):
        db_pool.get_connection()
    db_pool.close_all()
    assert db_pool.pool_length() == 0
    assert db_pool.used_length() == 0
