import os

# paths
DB = "vault.db"
STORAGE = "storage/files/"
if not os.path.exists(STORAGE):
    os.makedirs(STORAGE)

# vars
ITERS = 200000
SALT = 16
NONCE = 12  
