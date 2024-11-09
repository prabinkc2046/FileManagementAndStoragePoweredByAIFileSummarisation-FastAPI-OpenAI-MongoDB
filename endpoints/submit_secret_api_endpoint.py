# Standard library imports if any

# Third party imports
from fastapi import HTTPException, status, File, UploadFile, Depends, Form
from fastapi.responses import JSONResponse
from typing import Optional

# Local application import
from model import SecretModel
from mongodb.mongodb  import secret_collection
from user import get_current_active_user
from upload.save_ssh_credentials import save_ssh_private_key

# Store secret information in the database
async def get_upload_secret(
    open_api_key: Optional[str] = Form(None),
    remote_user: Optional[str] = Form(None),
    remote_host: Optional[str] = Form(None),
    ssh_password: Optional[str] = Form(None),
    password_key: Optional[str] = Form(None),
    saving_on_separate_remote_storage: bool = Form(...),
    file: UploadFile = File(None),  # File upload
    current_active_user: dict = Depends(get_current_active_user)  
):
    
    # Get the userid of the current active user
    user_id = current_active_user.get("user_id")

    # if user id is not found, raise an error
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    
    # Check if user is saving on the remote servere
    if saving_on_separate_remote_storage:
        if not remote_host:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Remote host must be provided when saving on separate remote storage is enabled."

            )
        if not remote_user:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Remote user must be provided when saving on separate remote storage is enabled."

            )
        
        if ssh_password is None and file is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Either SSH password or SSH private key file must be provided when saving on separate remote storage is enabled."
            )
        
    # Create ssh private key file if file  is provided
    path_to_ssh_private_file=None

    if file is not None:
        path_to_ssh_private_file = await save_ssh_private_key(file)
    
    # Create a SecretModel instance with the form data
     
    secret_info = SecretModel(
    user_id=user_id,
    open_api_key=open_api_key,
    remote_user=remote_user,
    remote_host=remote_host,
    ssh_password=ssh_password,
    ssh_key_path=path_to_ssh_private_file,
    password_key=password_key,
    saving_on_separate_remote_storage=saving_on_separate_remote_storage
    )
   
    # Creates secret document 
    secret_document = secret_info.model_dump()

    # Perform the upsert operation
    secret_collection.find_one_and_update(
        {"user_id": user_id},
        {"$set": secret_document},
        upsert=True,
    )

    return JSONResponse(
        content={"message":"Secret is successfully registered"},
        status_code=status.HTTP_200_OK
    )
