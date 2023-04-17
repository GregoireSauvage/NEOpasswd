import hashlib
import secrets
import base64
import json
import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Functions:
# generate_key, enter_username, check_master_key, get_key, enter_credentials


# Function to generate a key from a password
def generate_key(password, salt, iterations=100000, key_length=32):
    """
    Generate an encryption key from a password using PBKDF2.
    """
    # Encode the password and salt as bytes
    password_bytes = password.encode()

    # Use PBKDF2 to derive the key
    key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, key_length)

    # Return the key as bytes
    return key


# Function to enter username
def enter_username(data):
    """
    Enter username and heck if it exists in the data.
    """
    if(data == []):
        print("No users exist. Creating new user.")
    else:
        print("Users: " + ", ".join([user["username"] for user in data]))
    username = ""
    while username == "":
        username = input("Enter username: ")
    user_data = next((user for user in data if user["username"] == username), None)
    if user_data is not None:
        print("Username already exists. Please enter a different username.")
        return enter_username(data)
    return username


# Check that the master key is correct
def check_master_key(hash, salt):
    """
    Check that the master key is correct.
    """
    passephrase = getpass.getpass("Enter passphrase: ")
    
    # Derive the key from the passphrase and salt using PBKDF2
    master_key = get_key(passephrase, salt)

    # Hash the key
    hex_key = master_key.hex()
    encoded_key = hex_key.encode('utf-8')
    hashed_key = hashlib.sha256(encoded_key).hexdigest()

    # Check if the user's input matches the hashed key
    if hashed_key == hash:
        return master_key
    else:
        print("Incorrect passphrase")
        return check_master_key(hash, salt)


# Function to generate a key from a password
def get_key(password, salt, iterations=100000, key_length=32):
    """
    Generate an encryption key from a password using PBKDF2.
    """
    # Encode the password and salt as bytes
    password_bytes = password.encode()

    # Use PBKDF2 to derive the key
    key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, key_length)

    # Return the key as bytes
    return key

# Get email and password to encrypt from user
def enter_credentials(services):
    
    print("----- Services credentials already stored -----")
    for s in services:
        print(s)
    service = ""
    while service == "":
        service = input("Enter a new service name (gmail for example): ")
    # check if service already exists
    if service in services:
        print("Service already exists")
        return enter_credentials(services)
    
    email = ""
    while email == "":
        email = input("Enter email address: ")
    password = enter_password()
    return service, email, password

# Get password from user (create or generate)
def enter_password():
    
    print("Do you want to create your own password or generate a random one?")
    print("1. Create my own password")
    print("2. Generate a random password")
    choice = input("Enter your choice: ")
    if choice == "1":
        password = getpass.getpass("Enter password to encrypt: ")
        check_password = getpass.getpass("Re-enter password to encrypt: ")
        if(password != check_password):
            print("Passwords do not match")
            return enter_password()
        else:
            return password
    
    if choice == "2":
        length = 16
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&()+"
        password = "".join(secrets.choice(characters) for i in range(length))
        print("password : " + password)
        return password
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return enter_password()