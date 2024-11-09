# Fastapi module
from fastapi import HTTPException

# module for mongodb connection
from mongodb.mongodb import storage_collection

# Model
from model import StorageModel

async def register_storage_info(storage_info: StorageModel):
    try:
        existing_file = storage_collection.find_one({"file_id": storage_info.file_id})
        if existing_file:
            raise HTTPException(
                status_code=400,
                detail="File already registered"
            )

        # create a user document 
        file_storage_document = {
            "file_id": storage_info.file_id,
            "is_remote": storage_info.is_remote,
            "file_path":storage_info.file_path
        }

        storage_collection.insert_one(file_storage_document)
        print("data is insrted")
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while registering file storage info: {str(e)}"
        )