from fastapi import UploadFile, HTTPException
import subprocess, shutil, os, shlex

# Get storage model
from model import StorageModel

# Module to register file storage into into database
from upload.register_storage_info import register_storage_info

# Module to encrypt the file
from secret.encrypt_file import encrypt_file

# Get secret
from secret.retrieve_secret import retrieve_secret
from user import get_current_active_user
from fastapi import Depends


# find out the remote host directory
def get_home_directory(SSH_PASSWORD, REMOTE_USER, REMOTE_HOST) -> str:
    try:
        result = subprocess.run(
            ["sshpass", "-p", SSH_PASSWORD, "ssh", f"{REMOTE_USER}@{REMOTE_HOST}", "echo $HOME"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        home_directory = result.stdout.strip()
        return home_directory
    except subprocess.CalledProcessError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get remote home directory:{e.stderr}"


            )  
# Create the path to the storage directory on the remote server
def create_path_to_storage_directory(category: str, storage_directory_name, home_directory_path:str) ->  str:
    # Check if category is provided, otherwise use Uncategorised folder
    category = category if category else "Uncategorised"

    # create a path to the storage directory
    path_to_storage_directory:str = os.path.join(home_directory_path, storage_directory_name, category)
    return path_to_storage_directory

# Create a remote directory if it does not exists
def create_remote_directory(remote_storage_path: str, SSH_PASSWORD, REMOTE_USER, REMOTE_HOST ):
    try:
        quoted_remote_storage_path = shlex.quote(remote_storage_path)
        subprocess.run(
            ["sshpass", "-p", SSH_PASSWORD, "ssh", f"{REMOTE_USER}@{REMOTE_HOST}", f"mkdir -p {quoted_remote_storage_path}"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=400,
            detail="Failed to create remote directory"
        )

def send_file_to_remote_directory(path_to_local_file:str, remote_storage_path:str,SSH_PASSWORD, REMOTE_USER, REMOTE_HOST):
    try:
        quoted_remote_storage_path = shlex.quote(remote_storage_path)
        subprocess.run(
            ["sshpass", "-p", SSH_PASSWORD, "scp", path_to_local_file, f"{REMOTE_USER}@{REMOTE_HOST}:{quoted_remote_storage_path}"],
            check=True
        )
        
        # remove the local file after sending
        os.remove(path_to_local_file)

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=400,
            detail="Failed to send file to a remote server"
        )

# Gives path to the remote directory
def get_file_full_path(storage_dir: str, file: UploadFile):
    return os.path.join(storage_dir, file.filename)

async def store_file_temporarily(file: UploadFile) -> str:
    # define a path to the temporary storage
    filename = file.filename
    temp_file_path = f"/tmp/{filename}"
    # encrypt the file and store in the temporary path
    await encrypt_file(file, temp_file_path)
    # with open(temp_file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    return temp_file_path




async def save_remotely(secret_info:dict, storage_directory_name, file: UploadFile, category:str, fileid:str):
    """This saves file in the remote server with password based authentication"""

    # Retrieve secret 
    SSH_PASSWORD=secret_info.get("ssh_password")
    REMOTE_HOST=secret_info.get("remote_host")
    REMOTE_USER=secret_info.get("remote_user")

    #Get the home directory  of the remote server
    home_directory_path = get_home_directory(SSH_PASSWORD, REMOTE_USER, REMOTE_HOST)
    
    # Define a path to the storage directory
    path_to_storage_directory = create_path_to_storage_directory(category=category, storage_directory_name=storage_directory_name, home_directory_path=home_directory_path)

    # Create a path to the storage directory if it does not exist
    create_remote_directory(path_to_storage_directory, SSH_PASSWORD, REMOTE_USER, REMOTE_HOST)

    # Create a temporary file to store file content before sending
    # return the temporary file path
    temp_file_path = await store_file_temporarily(file)
    
    # Send file to the remote server
    send_file_to_remote_directory(temp_file_path, path_to_storage_directory, SSH_PASSWORD, REMOTE_USER, REMOTE_HOST)

    # Get full path to the file
    full_file_path = get_file_full_path(path_to_storage_directory, file)

    storage_info = StorageModel(
        file_id=fileid,
        is_remote=True,
        file_path=full_file_path
    )
    await register_storage_info(storage_info)