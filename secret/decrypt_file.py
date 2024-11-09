from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import aiofiles

async def decrypt_file(encrypted_file_path, filename):
    try:
        
        # Read the encrypted data from the file
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Extract the salt, nonce, tag, and ciphertext from the encrypted data
        salt = encrypted_data[:16]
        nonce = encrypted_data[16:28]
        tag = encrypted_data[28:44]
        ciphertext = encrypted_data[44:]
        
        
        # Derive the key using PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        password = filename
        key = kdf.derive(password.encode())

        # Create a Cipher object using AES-GCM
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Write the decrypted data to a new file
        async with aiofiles.open(encrypted_file_path, 'wb') as f:
            await f.write(decrypted_data)

    except Exception as e:
        print(f"Decryption error: {e}")
        raise e
