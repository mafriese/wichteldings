import os
from cryptography.fernet import Fernet

KEY_FILE = 'secret.key'

def load_key():
    """Loads the key from the current directory or generates a new one."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        return key

key = load_key()
cipher_suite = Fernet(key)

def encrypt_data(data: str) -> str:
    """Encrypts a string."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    """Decrypts a token back to a string."""
    try:
        return cipher_suite.decrypt(token.encode()).decode()
    except Exception:
        return None
