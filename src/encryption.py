from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()   
    print(key.decode())           
    return key

def load_key():
    import os
    if not os.path.exists("key.key"):
        print("ERROR: key.key file not found!")
        print("Run generate_key_file.py first to create encryption key.")
        exit()
    
    with open("key.key", "rb") as key_file:
        return key_file.read()
    


def encrypt_password(password,key):
    cipher = Fernet(key)
    encrypted = cipher.encrypt(password.encode())
    return encrypted.decode()


def decrypt_password(encrypted_password,key):
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_password.encode())
    return decrypted.decode()