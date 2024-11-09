# Import in-built module
from fastapi import UploadFile, HTTPException

# Get helper module
from upload.save_locally import save_locally
from upload.save_remotely import save_remotely
from upload.save_remotely_key import save_remotely_key
from secret.retrieve_secret import retrieve_secret


async def save_file(category:str, storage_directory_name, file: UploadFile, fileid:str, secret_info):
    try:
        saving_on_remote_server = secret_info.get("saving_on_separate_remote_storage")
        # This saves the file in the fast api server
        if saving_on_remote_server:
            ssh_key_path = secret_info.get("ssh_key_path")
           # if SSH_KEY_PATH is present, send file to remote server with ssh key
            if ssh_key_path is not None:
                await save_remotely_key(category, file, fileid, storage_directory_name, secret_info)
            #  if SSH_KEY_PATH is absent, use username and password to send file
            else:
                await save_remotely(secret_info, storage_directory_name=storage_directory_name, file=file, category=category, fileid=fileid)           
        else:
            await save_locally(category, file, fileid, storage_directory_name)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fail to save file: {e}"
        )
    