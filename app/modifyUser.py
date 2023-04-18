import hashlib
import getpass
import secrets
from fileManaging import load_users, save_data, load_data
from utilities import generate_key, enter_username, check_master_key

def modify_user(filename):
    users = load_users(filename)
    username, hashed_key, salt, id_service, services = load_data(filename)
    
    # Find the user data with the given username
    user_data = next((user for user in users if user["username"] == username), None)
    if user_data is None:
        print("Username does not exist. Please enter a different username.")
        return modify_user(filename)
    
    # Check the user master passphrase 
    check_master_key(hashed_key, salt)

    # Get the new username
    print("< NEW PROFILE >")
    new_username = ""
    while new_username == "" and new_username != username:
        new_username = input("Enter new username: ")
        
    # Get the new master passphrase
    new_master_key = ""
    new_master_key_check = ""
    while new_master_key != new_master_key_check or new_master_key == "":
        new_master_key = getpass.getpass("Enter new master passphrase: ")
        new_master_key_check = getpass.getpass("Re-enter new master passphrase: ")

    # Encrypt the new master key
    new_salt = secrets.token_bytes(16)
    new_key = generate_key(new_master_key, new_salt)

    # Hash the new key
    new_hex_key = new_key.hex()
    new_encoded_key = new_hex_key.encode('utf-8')
    new_hashed_key = hashlib.sha256(new_encoded_key).hexdigest()

    # Update the user's data
    user_data["username"] = new_username
    user_data["master_key"] = new_hashed_key
    user_data["salt"] = new_salt.hex()

    # Update the users list
    users = [user_data if user["username"] == username else user for user in users]

    # Save the updated data to the JSON file
    save_data(filename, users)

    print(f"User '{username}' has been updated with new username '{new_username}' and new master passphrase.")
