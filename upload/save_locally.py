# import built-in module 
import os, shutil


# Import module to register storage info like file path etc
from upload.register_storage_info import register_storage_info

# Import storagemodel
from model import StorageModel

# From cryptography
from secret.encrypt_file import encrypt_file
from fastapi import Depends
from user import get_current_active_user
from typing  import Dict

async def save_locally(category, file, fileid:str, storage_directory_name):
    """Saves file on the Fast API server at the home directory
    it uses default directory name unless provided
    it also uses category variable to create sub folder
    """
    # find the path to the home directory
    home_directory = os.path.expanduser("~")

    #path to the storage directory 
    storage_directory = os.path.join(home_directory, storage_directory_name)

    # folder by category
    category = category if category else "Uncategorised"

    # Path to categorised directory
    path_to_categorised_directory = os.path.join(storage_directory, category)

    # Ensure storage directory exists
    os.makedirs(path_to_categorised_directory, exist_ok=True)
    
    # Save the file to the directory
    file_path = os.path.join(path_to_categorised_directory, file.filename)
    
    # Ensure file is encrypted before saving it
    await encrypt_file(file, file_path)
    
    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    storage_info = StorageModel(
        file_id=fileid,
        is_remote=False,
        file_path=file_path
    )
    await register_storage_info(storage_info)