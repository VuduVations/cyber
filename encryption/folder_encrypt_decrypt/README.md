# VuduVations AES-CBC Folder Encryption and Decryption

<div align="center">
  <img src="CBA/assets/logo.png" alt="CyberChoice SMB Logo" height="333px">
</div>

This repository contains Python scripts for encrypting and decrypting files within a folder. The scripts use AES encryption in CBC mode for securing files. Additionally, the scripts handle backing up original files and creating necessary directories.

## Features

- **Custom File Encryption**: Encrypt individual files using AES encryption in CBC mode.
- **Backup Original Files**: Backup the original unencrypted files to a specified directory.
- **Decryption**: Decrypt encrypted files and save them to a specified output directory.
- **Directory Creation**: Automatically create backup and decrypted directories if they do not exist.

## Requirements

- Python 3.6+
- `cryptography` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/VuduVations/cyber/encryption/encrypt-decrypt-folder.git
    cd encrypt-decrypt-folder
    ```

2. Install the required Python packages:
    ```bash
    pip install cryptography
    ```

## Usage

### Encryption

1. **Encrypt a folder**:
    ```python
    import os
    from encrypt_decrypt import encrypt_folder
    
    input_folder = '/path/to/input/folder'
    backup_folder = '/path/to/backup/folder'
    password = b'your_password'

    encrypt_folder(input_folder, backup_folder, password)
    ```

    - `input_folder`: Path to the folder containing files to be encrypted.
    - `backup_folder`: Path to the folder where backups of the original files will be stored.
    - `password`: Password used for deriving the encryption key.

2. **Encrypt a single file** (if needed separately):
    ```python
    from encrypt_decrypt import encrypt_file, derive_key
    
    file_path = '/path/to/file'
    password = b'your_password'
    salt = os.urandom(16)
    key = derive_key(password, salt)
    
    encrypt_file(file_path, key)
    ```

### Decryption

1. **Decrypt a folder**:
    ```python
    from encrypt_decrypt import decrypt_folder

    input_folder = '/path/to/encrypted/folder'
    output_folder = '/path/to/decrypted/folder'
    password = b'your_password'

    decrypt_folder(input_folder, output_folder, password)
    ```

    - `input_folder`: Path to the folder containing encrypted files.
    - `output_folder`: Path to the folder where decrypted files will be saved.
    - `password`: Password used for deriving the decryption key.

2. **Decrypt a single file** (if needed separately):
    ```python
    from encrypt_decrypt import decrypt_file, derive_key

    file_path = '/path/to/encrypted/file'
    output_path = '/path/to/output/file'
    password = b'your_password'
    salt = read_salt_from_file('/path/to/salt.bin')
    key = derive_key(password, salt)

    decrypt_file(file_path, key, output_path)
    ```

## Example

```python
# Encrypt Folder
input_folder = '/path/to/input/folder'
backup_folder = '/path/to/backup/folder'
password = b'your_password'

encrypt_folder(input_folder, backup_folder, password)

# Decrypt Folder
encrypted_folder = '/path/to/encrypted/folder'
decrypted_folder = '/path/to/decrypted/folder'

decrypt_folder(encrypted_folder, decrypted_folder, password)
