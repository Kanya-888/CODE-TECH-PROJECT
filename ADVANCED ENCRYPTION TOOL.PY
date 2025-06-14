import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

BLOCK_SIZE = AES.block_size

def pad(data):
    padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding] * padding)

def unpad(data):
    return data[:-data[-1]]

def get_key(password, salt):
    return PBKDF2(password, salt, dkLen=32, count=1000000)

def encrypt_file(file_path, password):
    salt = get_random_bytes(16)
    key = get_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC)
    
    with open(file_path, 'rb') as f:
        plaintext = pad(f.read())

    ciphertext = cipher.encrypt(plaintext)
    encrypted_data = base64.b64encode(salt + cipher.iv + ciphertext)

    with open(file_path + '.enc', 'wb') as ef:
        ef.write(encrypted_data)

    print(f"[+] File encrypted: {file_path}.enc")

def decrypt_file(file_path, password):
    with open(file_path, 'rb') as ef:
        encrypted_data = base64.b64decode(ef.read())

    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    key = get_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext))

    original_file = file_path.replace('.enc', '')
    with open(original_file, 'wb') as f:
        f.write(plaintext)

    print(f"[+] File decrypted: {original_file}")

    salt = get_random_bytes(16)
    key = get_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC)
    
    with open(file_path, 'rb') as f:
        plaintext = pad(f.read())

    ciphertext = cipher.encrypt(plaintext)
    encrypted_data = base64.b64encode(salt + cipher.iv + ciphertext)

    with open(file_path + '.enc', 'wb') as ef:
        ef.write(encrypted_data)

    print(f"[+] File encrypted: {file_path}.enc")

def decrypt_file(file_path, password):
    with open(file_path, 'rb') as ef:
        encrypted_data 