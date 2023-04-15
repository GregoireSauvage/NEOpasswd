import getpass
import hashlib
import json
import secrets
from fileManaging import load_users
from fileManaging import save_master_key_and_salt_to_file
from utilities import enter_username
from utilities import generate_key


# Create user

try:
    data = load_users("passwordManager.json")
    username = enter_username(data)
    passphrase = getpass.getpass("Enter passphrase: ")
    salt = secrets.token_bytes(16)
    key = generate_key(passphrase, salt)

    # Print the salt
    print(salt)

    json_file = "passwordManager.json"

    # Hash the key
    hex_key = key.hex()
    encoded_key = hex_key.encode('utf-8')
    hashed_key = hashlib.sha256(encoded_key).hexdigest()

    # Save the username and salt to a JSON file
    save_master_key_and_salt_to_file(json_file, hashed_key, username, salt)

except ValueError as e:
    print(e)
    exit(0)
except KeyboardInterrupt:
    print("\nExiting...")
    exit(0)