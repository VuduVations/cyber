from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_data(data, key):
    # Create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC)
    # Encrypt the data
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = cipher.iv
    ciphertext = ct_bytes
    return iv, ciphertext

def decrypt_data(iv, ciphertext, key):
    # Create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt the data
    pt = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    return pt

# Example usage
key = get_random_bytes(16)  # AES key must be either 16, 24, or 32 bytes long
data = 'Hello World'

# Encrypt the data
iv, ciphertext = encrypt_data(data, key)
print(f'Encrypted data: {ciphertext.hex()}')

# Decrypt the data
plaintext = decrypt_data(iv, ciphertext, key)
print(f'Decrypted message: {plaintext}')
