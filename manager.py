import json
import os
from getpass import getpass
from cryptography.fernet import Fernet

PASSWORD_FILE = 'passwords.json'
KEY_FILE = 'key.key'


def Generate_Key():
    key = Fernet.Generate_Key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)


def Load_Key():
    return open(KEY_FILE, 'rb').read()


def Encrypt_Password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())


def Decrypt_Password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()


def Save_Passwords(passwords):
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(passwords, file)


def Load_Passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}


def Add_Password(account, password, key):
    passwords = Load_Passwords()
    encrypted_password = Encrypt_Password(password, key)
    passwords[account] = encrypted_password.decode()
    Save_Passwords(passwords)

    print(f"Password for {account} added successfully.")


def retrieve_password(account, key):
    passwords = Load_Passwords()

    if account in passwords:
        encrypted_password = passwords[account].encode()
        return Decrypt_Password(encrypted_password, key)
    else:
        print(f"Password not found for: {account}")
        return None

def main():
    
