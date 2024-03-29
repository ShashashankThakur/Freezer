import sqlite3


def create_database():
    try:
        # Connect to the SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect("_database_client.db")

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


if __name__ == "__main__":
    create_database()
