import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from fileManaging import load_data, save_password_data_to_file
from utilities import enter_credentials, check_master_key, get_key

# Function to encrypt a password
def encrypt_password(key, password):
    """
    Encrypt a password using AES encryption.
    """
    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)

    # Create an AES cipher object using the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the password to a multiple of the block size
    padded_password = password.encode().ljust(AES.block_size, b'\0')

    # Encrypt the padded password and IV using the cipher
    ciphertext = cipher.encrypt(padded_password)

    # Return the IV and ciphertext as bytes
    return iv, ciphertext

# Function to add a password (called from main.py)
def add_password(filename):
        
    try:
        # Get username, hashed master key, salt and id_service from the json file
        username, hashed_key, salt, id_service, services = load_data(filename)

        # Get username and passphrase from user
        master_key =  check_master_key(hashed_key, salt)

        # Once the master key is correct, get the email and password to encrypt
        service, email, password = enter_credentials(services)

        # Encrypt the password
        iv, cyphertext = encrypt_password(master_key, password)
        encrypted_password = iv + cyphertext

        print("------------------ ENCRYPTED PASSWORD ------------------")
        print(encrypted_password)

        # Save the encrypted password to the JSON file
        save_password_data_to_file(username, filename, id_service, service, email, encrypted_password)

    except ValueError as ve:
        print(ve)
        exit(0)
    except KeyboardInterrupt as ke:
        print("\nExiting...")
        exit(0)
