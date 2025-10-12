from encryption import load_key

ENCRYPTION_KEY = load_key()


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          
    'password': '12345',          
    'database': 'password_manager_db'
}