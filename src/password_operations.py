import mysql.connector
from database import get_db_connection
from encryption import encrypt_password, decrypt_password
from config import ENCRYPTION_KEY

def add_password(user_id, website, web_username, web_password):
   
    # Input validation
    if not website or not web_username or not web_password:
        print("\nError: All fields are required (website, username, password).")
        return False
    
    if len(website) > 200:
        print("\nError: Website name is too long (max 200 characters).")
        return False
    
    connection = get_db_connection()
    if connection is None:
        print("\nError: Database connection failed.")
        return False
    
    cursor = connection.cursor()
    
    try:
        encrypted_pwd = encrypt_password(web_password,ENCRYPTION_KEY)
        
        cursor.execute(
            "INSERT INTO passwords (user_id, website, web_username, web_password) VALUES (%s, %s, %s, %s)",
            (user_id, website, web_username, encrypted_pwd)
        )
        connection.commit()
        print("\nPassword added successfully!")
        cursor.close()
        connection.close()
        return True
    except Exception as err:
        print("\nError adding password:",err)
        cursor.close()
        connection.close()
        return False

def view_passwords(user_id):

    connection = get_db_connection()
    if connection is None:
        print("\nError: Database connection failed.")
        return
    
    cursor = connection.cursor()
    
    try:
        # Fetch all passwords for the user
        cursor.execute(
            "SELECT id, website, web_username, password FROM passwords WHERE user_id = %s",
            (user_id,)
        )
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        if results:
            print("\n" + "="*60)
            print("YOUR SAVED PASSWORDS")
            print("="*60)
            for row in results:
                pwd_id, website, web_username, encrypted_pwd = row
                try:
                    
                    decrypted_pwd = decrypt_password(encrypted_pwd,ENCRYPTION_KEY)
                except Exception:
                    decrypted_pwd = "[DECRYPTION FAILED - Key may have changed]"
                
                print(f"\nID: {pwd_id}")
                print(f"Website: {website}")
                print(f"Username: {web_username}")
                print(f"Password: {decrypted_pwd}")
                print("-"*60)
        else:
            print("\nNo passwords saved yet.")
    except mysql.connector.Error as err:
        print(f"\nDatabase error: {err}")

def search_password(user_id, website):
    # Input validation
    if not website:
        print("\nError: Please enter a website name to search.")
        return
    
    connection = get_db_connection()
    if connection is None:
        print("\nError: Database connection failed.")
        return
    
    cursor = connection.cursor()
    
    try:
        # Search for passwords matching the website name
        cursor.execute(
            "SELECT id, website, web_username, web_password FROM passwords WHERE user_id = %s AND website LIKE %s",
            (user_id, f"%{website}%")
        )
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        if results:
            print("\n" + "="*60)
            print(f"SEARCH RESULTS FOR: {website}")
            print("="*60)
            for row in results:
                pwd_id, website, web_username, encrypted_pwd = row
                try:
                    # Decrypt password for display
                    decrypted_pwd = decrypt_password(encrypted_pwd,ENCRYPTION_KEY)
                except Exception:
                    decrypted_pwd = "[DECRYPTION FAILED]"
                
                print(f"\nID: {pwd_id}")
                print(f"Website: {website}")
                print(f"Username: {web_username}")
                print(f"Password: {decrypted_pwd}")
                print("-"*60)
        else:
            print(f"\nNo passwords found for '{website}'.")
    except mysql.connector.Error as err:
        print(f"\nDatabase error: {err}")

def delete_password(user_id, password_id):

    connection = get_db_connection()
    if connection is None:
        print("\nError: Database connection failed.")
        return False
    
    cursor = connection.cursor()
    
    try:
        # First check if password exists
        cursor.execute(
            "SELECT website FROM passwords WHERE id = %s AND user_id = %s",
            (password_id, user_id)
        )
        result = cursor.fetchone()
        
        if not result:
            print("\nPassword not found or you don't have permission to delete it.")
            cursor.close()
            connection.close()
            return False
        
        # Ask for confirmation
        website = result[0]
        confirm = input(f"\nAre you sure you want to delete password for '{website}'? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("\nDeletion cancelled.")
            cursor.close()
            connection.close()
            return False
        
        # Delete password entry
        cursor.execute(
            "DELETE FROM passwords WHERE id = %s AND user_id = %s",
            (password_id, user_id)
        )
        connection.commit()
        print("\nPassword deleted successfully!")
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"\nError deleting password: {err}")
        cursor.close()
        connection.close()
        return False