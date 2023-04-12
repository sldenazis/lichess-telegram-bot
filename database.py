import sqlite3
import os

DB_PATH = os.environ.get('DB_PATH', 'database.sqlite')

def __run_write_query(query):
    connection = __get_connection()

    cursor = connection.cursor()
    cursor.execute(query)

    connection.commit()
    connection.close()

def __get_connection():
    db_path = DB_PATH
    connection = sqlite3.connect(db_path)

    return connection

def database_initialize():
    create_users = """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            lichess_username TEXT
        )
        """
    __run_write_query(create_users)

def database_update(query):
    connection = __get_connection()

    cursor = connection.cursor()
    cursor.execute(query)

    connection.commit()
    connection.close()

def database_fetchone(query):
    connection = __get_connection()

    cursor = connection.cursor()
    cursor.execute(query)

    result = cursor.fetchone()

    connection.commit()
    connection.close()

    return result

def database_fetchall(query):
    connection = __get_connection()

    cursor = connection.cursor()
    cursor.execute(query)

    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result
