from cryptography.fernet import Fernet

key = b'0Qhe8d18IR8GKcwv-5il_YhFTypXH2hpHjH_06KZXcw='
cipher = Fernet(key)

def encrypt(data):
    cipher_data = cipher.encrypt(data.encode())    # Converts into a sequence of bytes.
    return cipher_data

def decrypt(data):
    original_data = cipher.decrypt(data).decode()  # Converts the byte sequence back into the original message.
    return original_data