import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

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