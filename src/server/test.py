import sqlite3
import hashlib

USER_DATABASE = "_database_server.db"


def create_database(name):
    try:
        # Connect to the SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect(name)

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Create a table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
        ''')

        # Commit the transaction
        conn.commit()

        print("Database and table created successfully!")

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        # Close the connection
        if conn:
            conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect(USER_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()


# create_database("_database_server.db")
add_user("username", "password")

print("User added successfully.")
