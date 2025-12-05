import sqlite3
from config import DB


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        salt BLOB,
        password_hash BLOB
    )
    """)
    
    # files
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        owner TEXT,
        filename TEXT,
        original_name TEXT,
        PRIMARY KEY (owner, filename)
    )
    """)
    
    conn.commit()
    conn.close()


def insert_user(username, salt, password_hash):
    init_db()
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, salt, password_hash))
    conn.commit()
    conn.close()
    return True


def get_user(username):
    init_db()
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT salt, password_hash FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row


def insert_file(owner, filename, original_name):
    init_db()
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files VALUES (?, ?, ?)", (owner, filename, original_name))
    conn.commit()
    conn.close()


def get_user_files(owner):
    init_db()
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, original_name FROM files WHERE owner=?", (owner,))
    rows = cursor.fetchall()
    conn.close()
    return rows
