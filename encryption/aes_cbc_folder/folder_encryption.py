# VuduVations AES CBC Folder Encryption
# Author: S Halverson @vuduvations
# License: BSD 3-Clause

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import shutil

def derive_key(password, salt):
    """
    Derives a cryptographic key from the given password and salt using PBKDF2 with HMAC-SHA256.

    Args:
        password (bytes): The password to derive the key from.
        salt (bytes): The salt to use for key derivation.

    Returns:
        bytes: The derived key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return key

def encrypt_file(file_path, key):
    """
    Encrypts a file using AES encryption in CBC mode with PKCS7 padding.

    Args:
        file_path (str): The path to the file to be encrypted.
        key (bytes): The encryption key.

    Returns:
        None
    """
    iv = os.urandom(16)  # CBC requires a 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Pad the data to be a multiple of the block size (16 bytes for AES)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path, 'wb') as f:
        f.write(iv)
        f.write(ciphertext)

def backup_file(file_path, backup_folder):
    """
    Creates a backup of the specified file in the given backup folder.

    Args:
        file_path (str): The path to the file to be backed up.
        backup_folder (str): The path to the backup folder.

    Returns:
        None
    """
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    backup_path = os.path.join(backup_folder, os.path.basename(file_path))
    shutil.copy2(file_path, backup_path)

def encrypt_single_file(file_path, password):
    """
    Encrypts a single file, backing up the original file to a 'backup' folder in the same directory.

    Args:
        file_path (str): The path to the file to be encrypted.
        password (bytes): The password to derive the encryption key from.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    
    backup_folder = os.path.join(os.path.dirname(file_path), 'backup')
    salt = os.urandom(16)  # Secure random salt
    key = derive_key(password, salt)

    # Write the salt to the backup folder
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    with open(os.path.join(backup_folder, 'salt.bin'), 'wb') as f:
        f.write(salt)

    # Backup the original file
    backup_file(file_path, backup_folder)

    # Encrypt the original file in place
    encrypt_file(file_path, key)
    print(f"Encrypted: {file_path}")

# Example usage
file_path = '/path/to/your/file.txt'  # Replace with the path to your file to be encrypted
password = b'apassword'  # Replace with your password

encrypt_single_file(file_path, password)

# Best Practices Information:
# 1. **Password Management**: Ensure the password used for encryption is securely managed and not hard-coded in production environments.
# 2. **Backup Storage**: Store backups in a secure location to prevent unauthorized access.
# 3. **Key Management**: Use a secure method for storing and managing encryption keys.
# 4. **Regular Backups**: Maintain regular, encrypted backups of all critical data.
# 5. **Access Control**: Implement strict access controls to ensure only authorized personnel can access the encryption keys and encrypted data.
# 6. **Patch Management**: Keep all systems and software up to date with the latest security patches and updates.
# 7. **User Training**: Educate employees on recognizing phishing attempts and safe computing practices to reduce the risk of ransomware infections.
