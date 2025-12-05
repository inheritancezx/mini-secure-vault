import os
from config import NONCE
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

STORAGE_DIR = "storage/files/"

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def encrypt_file(filepath, key):
    with open(filepath, "rb") as f:
        plaintext = f.read()

    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE)  
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    filename = os.path.basename(filepath)
    encrypted_path = os.path.join(STORAGE_DIR, "[Encrypted] " + filename)

    with open(encrypted_path, "wb") as f:
        f.write(nonce + ciphertext)

    return encrypted_path, filename


def decrypt_file(encrypted_path, key, output_path):
    with open(encrypted_path, "rb") as f:
        data = f.read()

    nonce = data[:12]
    ciphertext = data[12:]

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_path, "wb") as f:
        f.write(plaintext)

    return output_path
