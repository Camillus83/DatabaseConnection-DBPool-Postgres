# DB Connection Pool implementation

That python script is an implementation of a database connection pool, which is designed to connect to a Postgres database. It provides a convenient and efficient way to manage database connections in a multi-threaded environment. By using a connection pool you can avoid the overhead of creating a new connection for each request, and improve the performance and scalability of Postgres database.

## Project structure

- <b>app directory</b>
  - main.py - Main script for db_pool execute, it shows logic how it works.
- <b>database directory</b>
  - db_connection.py - Module for managing dataabase connection pool using psycopg2
  - db_exceptions.py - Exceptions for database connections pool.
  - db_utils.py - This module provides class which contains methods for managing a PostgreSQL database.
- <b>tests directory</b>
  - fixtures.py - Fixtures for pytest tests.
  - test_db_connection_pool.py - Database Connection pool tests.
- <b>.env</b> - example of environmental variables which are required.
- <b>docker-compose.yml</b> - docker-compose file to run containers with python app and postgresql database
- <b>requirements.txt</b> - project dependencies

## How to run it?

1.  Make sure that you have Docker and docker-compose installed on your machine.
2. Clone this repository to your local machine.
3. Navigate to the root directory of the cloned repository.
4. Open a terminal window or command prompt in this directory.
5. Type the command `docker-compose up` and hit enter.
6. That's all!

## How to test it?

1. Navigate to the root directory of the cloned repository

2. Open a terminal window or command prompt in this directory.

3. Type the command `python -m pytest`

   



