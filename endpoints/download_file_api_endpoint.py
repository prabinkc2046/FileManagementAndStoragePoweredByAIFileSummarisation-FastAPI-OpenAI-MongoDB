# Fast api module
from fastapi import HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
import os
from scp import SCPClient

# Module to connect to database
from mongodb.mongodb import storage_collection


# from ssh
from ssh import (
    create_scp_client,
      get_file_from_remote, 
      identify_key_type, 
      load_private_key
)

# From user
from user import get_current_active_user

#  From secret
from secret.decrypt_file import decrypt_file

from caching import get_secret_info

# Define a background task to delete file
def delete_local_file(file_path:str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted temporary file:{file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path} : {str(e)}")

# Get files from local or remote server
async def get_download(
    file_id:str,
    background_task: BackgroundTasks,
    secret_info:dict = Depends(get_secret_info),
    current_active_user: dict = Depends(get_current_active_user),
):
    try:
        # Checks file exists
        file_data = storage_collection.find_one({"file_id": file_id})

        # Throw error if file is not found
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        # Get the path of file
        file_path = file_data["file_path"]

        # Throw error if file_location is not found
        if not file_path:
            raise HTTPException(status_code=404, detail="File location is not found")

        # Get storage location remote or local
        is_remote: bool = file_data["is_remote"]

        # If file is stored in remote location, do this ..
        if is_remote:
            # Get ssh_key_path from secret_info
            ssh_key_path = secret_info.get("ssh_key_path")
            ssh_password_key = secret_info.get("password_key")
            ssh_password = secret_info.get("ssh_password")
            remote_host = secret_info.get("remote_host")
            remote_user=secret_info.get("remote_user")
            password_key=secret_info.get("password_key")

            # Authenticate with with SSH KEY and passphrase
            if ssh_key_path:
                # Get the type of key used in ssh
                key_type = identify_key_type(ssh_key_path=ssh_key_path, pass_phrase=ssh_password_key)

                # Load the private key once we know the type of the key
                pkey = load_private_key(key_type,
                        ssh_key_path,
                        ssh_password_key)

                # Use private key to create scp and ssh client
                scp, ssh = await create_scp_client(
                    remote_host,
                    remote_user,
                    password_key,
                    pkey=pkey
                )

                # Download file from the remote server
                local_file_path = get_file_from_remote(
                    remote_path=file_path,
                    ssh_client=ssh,
                    scp_client=scp
                )
            else:
                # Authenticate with username and password
                # Use username and password to initiate scp and ssh client
                scp, ssh = create_scp_client(
                    remote_host,
                    remote_user,
                    ssh_password,
                    pkey
                )

                # Download file from the remote server
                local_file_path = get_file_from_remote(
                    remote_path=file_path,
                    ssh_client=ssh,
                    scp_client=scp
                )

            background_task.add_task(delete_local_file, local_file_path)
    

                

        # file is stored locally
        else:            
            # Checks if file path exists in the local computer as provided by file location
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="File not found")
            
            local_file_path = file_path

        filename = os.path.basename(local_file_path)
        
        await decrypt_file(encrypted_file_path=local_file_path, filename=filename)

        if os.path.getsize(local_file_path) == 0:
            raise HTTPException(status_code=500, detail="Decryption resulted in an empty file.")


        headers = {
            "Content-Disposition": f"attachment; filename={filename}"
        }
        return FileResponse(
            path=local_file_path,
            media_type='application/octet-stream',
            headers=headers
        )
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occured: {str(e)}"
        )
