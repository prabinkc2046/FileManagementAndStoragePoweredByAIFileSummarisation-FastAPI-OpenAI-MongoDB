# Import built-in Operating system related module
import os, shlex, shutil

# Import built-in fastapi module
from fastapi import HTTPException

# Import built-in paramiko module
import paramiko as pk
from scp import SCPClient


# Import for cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519

# Import typing
from  typing import Union

# Import module to register file storage into in database
from upload.register_storage_info import register_storage_info

# Import model to define our file storage info
from model import StorageModel

# import  module to encrypt file
from secret.encrypt_file import encrypt_file


# Importing from ssh
from ssh import (
    load_private_key,
    identify_key_type,
    create_ssh_client,
    save_file_to_remote_server
)


"""Get the path name of remote server's home directory"""
async def get_remote_home_directory(ssh_client):
    try:
        stdin, stdout, stderr = ssh_client.exec_command('echo $HOME')
        home_directory = stdout.read().strip().decode('utf-8')
        return home_directory
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get remote home directory: {str(e)}")

"""Makes a directory path to store file based on its category and storage directory name"""
def create_full_path_to_storage_directory(category, home_directory, storage_directory_name):
    # if category is not provided, use default category
    category = category if category else "Uncategorised"

    full_path = os.path.join(home_directory, storage_directory_name, category)
    return full_path

"""Creates directory if it does not exists"""
def ensure_remote_directory_exists(ssh_client, remote_directory_path):
    quoted_remote_directory_path = shlex.quote(remote_directory_path)
    try:
        stdin,  stdout, stderr = ssh_client.exec_command(f"mkdir -p {quoted_remote_directory_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create remote storage directory: {str(e)}")

"""Create a temporary file path to store the file content temporarily"""
def create_temporary_file_path(file):
    try:
        # get the file name
        filename = file.filename

        # Define the path to the temporary file
        temp_file_path = os.path.join("/tmp", filename)

        # Write the content of the file into this temporary folder
        # with open(temp_file_path, "wb") as buffer:
        #     shutil.copyfileobj(file.file, buffer)
        return temp_file_path
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Failed to create a temporary file path"
        )

"""Removes the temporary file path"""
def remove_temporary_file(temp_file_path):
    os.remove(temp_file_path)


"""Create a full path to the file in the storage directory"""
def create_full_path_to_file(path_to_storage_directory, file):
    return os.path.join(path_to_storage_directory, file.filename)


async def save_remotely_key(category, file, fileid:str, storage_directory_name,secret_info:dict):
    """Saves file on the remote server using ssh key authentication"""
    try:

        # Retrieve secret 
        REMOTE_HOST=secret_info.get("remote_host")
        REMOTE_USER=secret_info.get("remote_user")
        SSH_KEY_PATH=secret_info.get("ssh_key_path")
        SSH_PASSWORD_KEY=secret_info.get("password_key")

        # Get the type of the key
        key_type = identify_key_type(ssh_key_path=SSH_KEY_PATH, pass_phrase=SSH_PASSWORD_KEY)
        print("Key type is", key_type)

        # load the private key
        pkey = load_private_key(key_type, SSH_KEY_PATH, SSH_PASSWORD_KEY)
        print("private key is", pkey)

        # Initiate SSH client
        ssh_client_created = create_ssh_client(pkey, REMOTE_HOST, REMOTE_USER)

        # Get the path name of remote's server home directory
        remote_home_directory = await get_remote_home_directory(ssh_client=ssh_client_created)

        # Create a full path of the directory to store file
        full_path = create_full_path_to_storage_directory(storage_directory_name=storage_directory_name, category=category,home_directory=remote_home_directory)

        # Makes directory 
        ensure_remote_directory_exists(ssh_client=ssh_client_created,remote_directory_path=full_path)

        # Makes a temporary file on the fast api server to store file content temporarily
        temp_file_path = create_temporary_file_path(file)

        # Encrypt the file and store the encrypted content in the temporary file path
        await encrypt_file(file, temp_file_path)
        
        # Copy file from temp file path to the remote server
        save_file_to_remote_server(
            temp_file_path=temp_file_path,
            remote_storage_directory=full_path,
            ssh_client=ssh_client_created
        )

        # Gives the full path to the file inside the storage directory
        file_path = create_full_path_to_file(path_to_storage_directory=full_path, file=file)
        
        # Define the storage file info
        storage_info = StorageModel(
        file_id=fileid,
        is_remote=True,
        file_path=file_path
        )
        
        await register_storage_info(storage_info)

        # Removes the temporary file path
        remove_temporary_file(temp_file_path=temp_file_path)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



