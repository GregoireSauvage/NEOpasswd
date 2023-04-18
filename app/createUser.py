import getpass
import hashlib
import json
import secrets
from fileManaging import load_users
from fileManaging import save_master_key_and_salt_to_file
from utilities import enter_username
from utilities import generate_key


# Create user
def create_user(filename):
    """
    Create a new user.
    """
    # Load the existing user data
    try:
        data = load_users(filename)
        username = enter_username(data) 
        passphrase = ""
        passphrase_check = ""
        while passphrase != passphrase_check or passphrase == "":
            passphrase = getpass.getpass("Enter passphrase: ")
            passphrase_check = getpass.getpass("Re-enter passphrase: ")
        
        salt = secrets.token_bytes(16)
        key = generate_key(passphrase, salt)

        # Hash the key
        hex_key = key.hex()
        encoded_key = hex_key.encode('utf-8')
        hashed_key = hashlib.sha256(encoded_key).hexdigest()
        
        # Save the username and salt to a JSON file
        save_master_key_and_salt_to_file(filename, hashed_key, username, salt)

    except ValueError as e:
        print(e)
        exit(0)
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)