import sqlite3
import hashlib

FILE_DATABASE = "_database_client.db"


def create_database(name):
    try:
        # Connect to the SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect(name)

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Create a table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                filename TEXT PRIMARY KEY,
                hashed_filename TEXT NOT NULL UNIQUE,
                chunks INTEGER NOT NULL
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


def hash_password(filename):
    return hashlib.sha256(filename.encode()).hexdigest()


def add_file(filename, chunks):
    hashed_filename = hash_password(filename)
    with sqlite3.connect(FILE_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (filename, hashed_filename, chunks) VALUES (?, ?, ?)",
                       (filename, hashed_filename, chunks))
        conn.commit()


# create_database("_database_client.db")
add_file("logs.pdf", 1)
