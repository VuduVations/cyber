from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Function to encrypt data using AES
def aes_encrypt(key, plaintext):
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)  # AES block size is 16 bytes
    # Create an encryptor object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad the plaintext to be a multiple of the block size
    padder = padding.PKCS7(128).padder()  # Block size: 128 bits
    padded_data = padder.update(plaintext) + padder.finalize()
    # Encrypt the data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext

# Function to decrypt data using AES
def aes_decrypt(key, iv, ciphertext):
    # Create a decryptor object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    # Decrypt the data
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    # Unpad the plaintext
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

# Example usage
key = os.urandom(32)  # AES-256 key
plaintext = b'Hello, world!'  # Plaintext message (must be bytes)

# Encrypt the plaintext
iv, ciphertext = aes_encrypt(key, plaintext)
print(f'Encrypted: {ciphertext}')

# Decrypt the ciphertext
decrypted_plaintext = aes_decrypt(key, iv, ciphertext)
print(f'Decrypted: {decrypted_plaintext}')
