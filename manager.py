import json
import os
from getpass import getpass
from cryptography.fernet import Fernet

PASSWORD_FILE = 'passwords.json'
KEY_FILE = 'key.key'


def Generate_Key():
    key = Fernet.generate_key()
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
    if not os.path.exists(KEY_FILE):
        print("Encryption not found. Generating a new key...")
        Generate_Key()

    key = Load_Key()

    while True:
        print("--- Password Manager ---")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Exit")

        option = input("Enter your option: ")

        if option == "1":
            account = input("Enter account name (e.g., website or app name): ")
            password = getpass("Enter the password: ")
            Add_Password(account, password, key)

        elif option == "2":
            account = input("Enter account name: ")
            password = retrieve_password(account, key)

            if password:
                print(f"Password for {account}: {password}")

        elif option == "3":
            print("Exiting the Password Manager.")
            break

        else:
            account = input("Invalid choice. Enter correct choice: ")


if __name__ == "__main__":
    main()
