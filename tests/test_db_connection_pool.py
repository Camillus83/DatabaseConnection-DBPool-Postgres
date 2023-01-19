import pytest

from psycopg2.extensions import connection

from fixtures import db_container, db_pool, db_pool_2, MAX_CONNECTIONS, MIN_CONNECTIONS


def test_singleton(db_container, db_pool, db_pool_2):
    assert db_pool is db_pool_2


def test_min_max_connections(db_container, db_pool):
    assert db_pool.minconn == MIN_CONNECTIONS
    assert db_pool.maxconn == MAX_CONNECTIONS


def test_lists_creation(db_container, db_pool):
    assert len(db_pool._pool) == MIN_CONNECTIONS
    assert len(db_pool._used) == 0


def test_get_connection(db_container, db_pool):
    conn = db_pool.get_connection()
    assert conn is not None
    assert isinstance(conn, connection)
    db_pool.return_connection(conn)


def test_put_connection(db_container, db_pool):
    pool_len_before_conn = len(db_pool._pool)
    used_len_before_conn = len(db_pool._used)
    conn = db_pool.get_connection()
    assert len(db_pool._used) == used_len_before_conn + 1
    db_pool.return_connection(conn)
    assert len(db_pool._pool) == pool_len_before_conn


def test_connections_exhausted(db_container, db_pool):
    with pytest.raises(Exception, match="Too many connections."):
        for _ in range(MAX_CONNECTIONS + 1):
            db_pool.get_connection()

    db_pool.close_all()


def test_closing_all_connections(db_container, db_pool):
    for _ in range(MIN_CONNECTIONS + 1):
        db_pool.get_connection()
    db_pool.close_all()
    assert len(db_pool._used) == 0, db_pool._used
    assert len(db_pool._pool) == 0, db_pool._pool
