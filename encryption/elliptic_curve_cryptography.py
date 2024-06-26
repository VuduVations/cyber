'''
* Generate an ECC private key.
* Derive a shared secret using the private key and a peer’s public key (for demonstration, we use the same key pair).
* Use the shared secret to derive a symmetric key.
* Use the symmetric key (AES in this case) to encrypt and decrypt the message.
'''

!pip install cryptography

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# Generate an ECC key pair
private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
public_key = private_key.public_key()

# Serialize the public key to send it safely
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Derive a shared secret from the private key and the peer public key
# Note: In practice, you'd get the peer public key from the peer
peer_public_key = private_key.public_key()  # This should be the peer's public key
shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)

# Perform key derivation
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
    backend=default_backend()
).derive(shared_secret)

# Encrypt and decrypt a message using the derived key
# Note: ECC itself doesn't directly encrypt data, it's used to derive keys
# In practice, you'd use this derived key with a symmetric cipher like AES
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

aesgcm = AESGCM(derived_key)
nonce = b'\x00' * 12  # In practice, use a unique nonce for each message
plaintext = b'A secret message'
ciphertext = aesgcm.encrypt(nonce, plaintext, None)
decryptedtext = aesgcm.decrypt(nonce, ciphertext, None)

print(f"Original message: {plaintext}")
print(f"Encrypted message: {ciphertext}")
print(f"Decrypted message: {decryptedtext}")
