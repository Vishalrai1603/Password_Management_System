import mysql.connector
from config import DB_CONFIG

def get_connection():
    try:
        connection = mysql.connector.connect(
            host = DB_CONFIG['host'],
            user = DB_CONFIG['user'],
            password = DB_CONFIG['password']
        )
        return connection
    except mysql.connector.Error as err:
        print("Error: ", err)
        return None

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host = DB_CONFIG['host'],
            user = DB_CONFIG['user'],
            password = DB_CONFIG['password'],
            database = DB_CONFIG['database']
        )
        return connection
    except mysql.connector.Error as err:
        print("Error: ", err)
        return None

def setup_database():
    connection = get_connection()

    if connection:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS password_manager_db")
        print("Database 'password_manager_db' ready.")

        cursor.close() 
        connection.close()

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL
                )
            
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    website VARCHAR(100) NOT NULL,
                    web_username VARCHAR(100) NOT NULL,
                    web_password TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE 
                )
            
            ''')
            
            connection.commit()
            print("Table created successfully...")

            cursor.close()
            connection.close()