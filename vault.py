import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config import STORAGE, NONCE
from db import insert_file, get_user_files

def encrypt_file(filepath, key):
    with open(filepath, "rb") as f:
        plaintext = f.read()

    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    filename = os.path.basename(filepath)
    encrypted_path = os.path.join(STORAGE, "[Encrypted] " + filename)

    with open(encrypted_path, "wb") as f:
        f.write(nonce + ciphertext)

    return encrypted_path, filename


def decrypt_file(encrypted_path, key, output_path):
    with open(encrypted_path, "rb") as f:
        data = f.read()

    nonce = data[:NONCE]
    ciphertext = data[NONCE:]

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_path, "wb") as f:
        f.write(plaintext)

    return output_path


def upload_file(username, key):
    filepath = input("Path to the file: ").strip()
    if not os.path.exists(filepath):
        print("File not found.")
        return

    encrypted_path, original_name = encrypt_file(filepath, key)
    insert_file(username, os.path.basename(encrypted_path), original_name)
    print(f"File '{original_name}' encrypted & stored successfully!")


def view_files(username):
    rows = get_user_files(username)

    if not rows:
        print("No files uploaded yet.")
        return
    
    print("\nYour files:")
    for i, (enc_filename, original_name) in enumerate(rows, 1):
        print(f"  {i}. {original_name}")


def download_file(username, key):
    view_files(username)
    choice = input("Enter file number to download: ").strip()

    rows = get_user_files(username)
    if not rows:
        return

    try:
        chosen = rows[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid choice.")
        return

    enc_filename, original_name = chosen
    encrypted_path = os.path.join(STORAGE, enc_filename)

    output_path = input(f"Save decrypted file as [{original_name}]: ").strip()
    if not output_path:
        output_path = original_name

    decrypt_file(encrypted_path, key, output_path)
    print(f"File decrypted and saved as {output_path}")