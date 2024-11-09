
from fastapi import File, UploadFile, Form
import os, stat, shutil
from datetime import datetime
from fastapi import HTTPException


"""Checks if ~/.ssh exists or not and create one if does not exist"""
def create_directory_to_store_ssh_key():
    try:
        # Get the home directory
        home_dir = os.path.expanduser("~")

        # Path to the .ssh directory
        ssh_directory = os.path.join(home_dir, ".ssh")

        # Check if ssh directory exists and create if it does not
        if not os.path.exists(ssh_directory):
            # Creates directory
            os.makedirs(ssh_directory, mode=0o700, exist_ok=True)
            # Sets permission
            os.chmod(ssh_directory, mode=0o700)
        
        if not os.path.isdir(ssh_directory):
            raise Exception("SSH directory could not be created")
        
        return ssh_directory

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not create SSH directory: {str(e)}"
        )

"""Creates private key file with the content of ssh key"""
def create_private_key_file(ssh_dir, file):
    try:
        # Check the ssh directory exists
        if not os.path.exists(ssh_dir):
            raise HTTPException(status_code=400, detail="SSH directory does not exist")

        # Create a unique file name
        filename = f"id_rsa_{datetime.now().strftime('%Y%m%d%H%M%S')}" 

        # Create a path to the file
        private_key_path = os.path.join(ssh_dir, filename)

        # Write the ssh key data in the file
        with open(private_key_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read/write for the user, no permission for others
        os.chmod(private_key_path, stat.S_IRUSR | stat.S_IWUSR) 

        return private_key_path
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create private key file: {str(e)}"
        )

async def save_ssh_private_key(
    file: UploadFile = Form(...),
):
    try:
        # Create SSH directory if does  not exists
        ssh_directory = create_directory_to_store_ssh_key()

        # Create unique private key file
        private_key_path = create_private_key_file(ssh_directory, file)
        
        # Return the receive SSH key and password
        return private_key_path

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
