# config.py

from encryption_utils import encrypt_data, generate_key

# Generate a key for encryption/decryption
KEY = generate_key()

# Encrypt the credentials
APP_USERNAME = encrypt_data("ctyndorf@aerosoftsys.com", KEY)
APP_PASSWORD = encrypt_data("K8p0n3r1d!sAB", KEY)
