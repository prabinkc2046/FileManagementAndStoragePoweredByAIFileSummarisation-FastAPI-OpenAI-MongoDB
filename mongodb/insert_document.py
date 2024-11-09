from uuid import uuid4
from datetime import datetime, timezone
from model import FileModel
from mongodb.mongodb import files_collection
from pymongo.errors import PyMongoError
from fastapi import File, UploadFile
async def insert_document(category:str, file:UploadFile, summary:str):
    try:
        # Set the value of category
        category = category if category else "Uncategorised"

        # Create a file document to be inserted into a files_collection
        file_id = str(uuid4())
        current_date = datetime.now(tz=timezone.utc)
        file_document = FileModel(
            file_id=file_id,
            name=file.filename,
            summary=summary,
            date_uploaded=current_date,
            category=category,
        )

        # Insert into MongoDb
        result = files_collection.insert_one(file_document.model_dump())

        # return file id to store in storage collection
        return file_id
        
        if not result.inserted_id:
            raise Exception("Failed to insert document into MongoDB")
    except PyMongoError as e:
        raise Exception(f"There was an error in inserting document into collection, {e}")
