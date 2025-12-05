import os
import hashlib
from getpass import getpass
from config import ITERS, SALT
from db import insert_user, get_user


def register_user():
    username = input("Create username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return False
    
    password = getpass("Create password: ")
    if not password:
        print("Password cannot be empty.")
        return False

    salt = os.urandom(SALT)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERS)
    
    insert_user(username, salt, pwd_hash)
    return True


def login():
    username = input("Username: ").strip()
    password = getpass("Password: ")

    row = get_user(username)
    if row is None:
        return None, None, "user_not_found"

    salt, stored_hash = row
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERS)

    if pwd_hash != stored_hash:
        return None, None, "wrong_password"

    return username, pwd_hash, None
