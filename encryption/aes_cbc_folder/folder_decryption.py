# VuduVations AES CBC Folder Decryption
# Author: S Halverson @vuduvations
# License: BSD 3-Clause

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

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

def decrypt_file(file_path, key, output_folder):
    """
    Decrypts a file using AES decryption in CBC mode and PKCS7 padding.

    Args:
        file_path (str): The path to the file to be decrypted.
        key (bytes): The decryption key.
        output_folder (str): The path to the folder where the decrypted file will be saved.

    Returns:
        None
    """
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    file_data = unpadder.update(padded_data) + unpadder.finalize()

    relative_path = os.path.relpath(file_path, start=input_folder)
    output_path = os.path.join(output_folder, relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as f:
        f.write(file_data)

def decrypt_folder(input_folder, output_folder, password):
    """
    Decrypts all files in the specified input folder using the given password, and saves them to the output folder.

    Args:
        input_folder (str): The path to the folder containing encrypted files.
        output_folder (str): The path to the folder where decrypted files will be saved.
        password (bytes): The password to derive the decryption key.

    Returns:
        None
    """
    with open(os.path.join(input_folder, 'salt.bin'), 'rb') as f:
        salt = f.read()

    key = derive_key(password, salt)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file == 'salt.bin':
                continue

            file_path = os.path.join(root, file)
            decrypt_file(file_path, key, output_folder)
            print(f"Decrypted: {file_path}")

# Example usage
input_folder = '/path/to/encrypted/folder'  # Replace with the path to your encrypted folder
output_folder = '/path/to/decrypted/folder'  # Replace with the path to your decrypted folder
password = b'Vuduchild'  # Replace with your password

decrypt_folder(input_folder, output_folder, password)

# Best Practices Information:
# 1. **Password Management**: Ensure the password used for encryption is securely managed and not hard-coded in production environments.
# 2. **Backup Storage**: Store backups in a secure location to prevent unauthorized access.
# 3. **Key Management**: Use a secure method for storing and managing encryption keys.
# 4. **Regular Backups**: Maintain regular, encrypted backups of all critical data.
# 5. **Access Control**: Implement strict access controls to ensure only authorized personnel can access the encryption keys and encrypted data.
# 6. **Patch Management**: Keep all systems and software up to date with the latest security patches and updates.
# 7. **User Training**: Educate employees on recognizing phishing attempts and safe computing practices to reduce the risk of ransomware infections.
