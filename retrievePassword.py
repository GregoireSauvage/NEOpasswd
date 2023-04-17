import getpass
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from fileManaging import load_password_data

# Function to encrypt a password
def decrypt_password(encrypted_password, salt):
    """
    Decrypt a password using AES decryption and a user-provided passphrase.
    """
    # Prompt the user for the passphrase
    passphrase = getpass.getpass("Enter passphrase: ").encode()

    # Derive the key from the passphrase and salt using PBKDF2
    key = hashlib.pbkdf2_hmac("sha256", passphrase, salt, 100000)

    # Extract the IV and ciphertext from the encrypted password
    iv = encrypted_password[:AES.block_size]
    ciphertext = encrypted_password[AES.block_size:]

    # Create an AES cipher object using the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext using the cipher
    padded_password = cipher.decrypt(ciphertext)

    # Remove any padding from the decrypted password
    password = padded_password.rstrip(b'\0')

    # Return the password as a string
    return password.decode()

def retrieve_password(filename):
        
    try:
        salt, encrypted_password, service, username, email = load_password_data(filename)
    except ValueError as e:
        print(e)
        exit(0)
    except KeyboardInterrupt as ke:
        print("\nExiting...")    
        exit(0)

    try:
        decrypted_password = decrypt_password(encrypted_password, salt)
    except ValueError:
        print("Incorrect passphrase.")
        exit(0)

    try:
        print("------------------ DECRYPTED PASSWORD ------------------")
        print("Service: " + service)
        print("Username: " + username)
        print("Email: " + email)
        print("Password : " + decrypted_password)

    except Exception as e:
        print("Error: " + str(e))
        exit(1)
    except KeyboardInterrupt as ke:
        print("\nExiting...")    
        exit(0)