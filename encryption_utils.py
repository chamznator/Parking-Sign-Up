# encryption_utils.py

from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key for encryption/decryption.
    """
    return Fernet.generate_key()

def encrypt_data(data, key):
    """
    Encrypts the given data using the provided key.
    """
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """
    Decrypts the given encrypted data using the provided key.
    """
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data