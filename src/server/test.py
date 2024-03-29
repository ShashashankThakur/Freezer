import sqlite3
import hashlib

USER_DATABASE = "_database_server.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect(USER_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()


add_user("username", "password")

print("User added successfully.")
