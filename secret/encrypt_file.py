from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os
import base64
from fastapi import File, UploadFile
from io import BytesIO
import aiofiles
from fastapi import HTTPException

async def encrypt_file(file: UploadFile, file_path):
    # Check if the file is empty
    if file.size == 0:
        raise HTTPException(status_code=500, detail="Uploaded file is empty")
    
    # Generate a random salt
    salt = os.urandom(16)

    # Define a random password which is always consistent for this file
    password = file.filename

    # Derive a key using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Generate a random nonce
    nonce = os.urandom(12)

    # Create a Cipher object using AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    # Reset pointer before reading
    await file.seek(0)

    file_data = await file.read()

    if not file_data:
        raise HTTPException(status_code=500, detail="Failed to read data from file.")


    # Encrypt the file data
    ciphertext = encryptor.update(file_data) + encryptor.finalize()

    # Store the salt, nonce, and tag with the ciphertext
    encrypted_data = salt + nonce + encryptor.tag + ciphertext

    # Write the encrypted data to a new file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(encrypted_data)
