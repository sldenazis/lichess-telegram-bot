import sqlite3
import os

def users_db():
    db_path = os.environ.get('DB_PATH', 'database.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            lichess_username TEXT
        )
        """
    )
    conn.commit()

    return conn
