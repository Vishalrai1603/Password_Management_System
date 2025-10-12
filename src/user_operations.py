import mysql.connector
from database import get_db_connection
import hashlib
from config import ENCRYPTION_KEY


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(username, password):

    hashed_pw = hash_password(password)

    if not username or not password:
        print("\nError: Username and password cannot be empty.")
        return False

    if len(username) < 3:
        print("\nError: Username must be at least 3 characters long.")
        return False

    if len(password) < 6:
        print("\nError: Password must be at least 6 characters long.")
        return False

    connection = get_db_connection()
    if connection is None:
        print("\nError: Database connection failed. Please check your MySQL server.")
        return False
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        connection.commit()

        print("\n Singup successful! Welcome ,", username)

        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        print("\nSignup failed. Please try different credentials.")
        cursor.close()
        connection.close()
        return False


def login(username, password):
    hashed_pw = hash_password(password)

    if not username or not password:
        print("\nError: Username and password cannot be empty.")
        return None

    connection = get_db_connection()
    if connection is None:
        print("\nError: Database connection failed. Please check your MySQL server.")
        return None
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT id, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result and result[1] == hashed_pw:
            print(f"\nLogin successful! Welcome back, {username}!")
            return result[0]
        else:
            print("\nInvalid username or password.")
            return None
    except mysql.connector.Error as err:
        print(f"\nDatabase error: {err}")
        cursor.close()
        connection.close()
        return None
