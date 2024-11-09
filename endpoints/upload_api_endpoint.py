# built-in module
from fastapi import UploadFile, File, Form, Depends, Query, HTTPException, status
from fastapi.responses import JSONResponse

# Module required to verify user
from user import get_current_active_user

# Module from extraction
from extraction.validate_filetype import validate_filetype
from extraction.check_filetype_and_extract import check_filetype_and_extract

# Module from mongod
from mongodb.mongodb import files_collection
from mongodb.insert_document import insert_document

# From  upload
from upload.save import save_file

# From open ai
from open_ai.request_summary import summarise_text
# from Environment
async def get_upload(
        words: int, #number of words to extract from file
        category: str, #name to create folder,
        max_tokens: int, # max token to use for summarising file
        summary_counts: int, # number of words to use in summary
        storage_directory_name:str, # name of the parent directory under which subfolders will be created
        secret_info:dict,
        file: UploadFile = File(...),
        current_active_user: dict = Depends(get_current_active_user)
):
    try:
        # check the validity of the file type
        # throws error if the filetype is not pdf or doc or docx
        validate_filetype(file)

        # Check if file already exists in the database
        existing_file = files_collection.find_one({"name":file.filename})
        
        # if file is found in database, throw and http exception
        if existing_file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File already exists in the datbase"
            )
        
        # extract the text from the documents
        text = await check_filetype_and_extract(file, words)

        # if text could not be extracted, throw an exception
        if not text:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Failed to extract text from the file"
            )
        
        # Get the open api key from the cache
        # openai_api_key = secret_info.get("open_api_key")
        
        # if openai_api_key is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Open api key is required, Please provide one"
        #     )
        
        # Summarise the extracted text
        # summary = await summarise_text(openai_api_key=openai_api_key, summary_words_count=summary_counts, max_tokens=max_tokens, text=text)

        # if summary is not obtained from apen ai, throw error
        # if summary is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Failed to get summary from the open ai"
        #     )
        
        # Insert the document into collections
        file_id = await insert_document(category, file, summary="This is an example summary")
        
        # save file 
        await save_file(category, storage_directory_name, file, file_id, secret_info)

        return JSONResponse(
            content={"message":"File is uploaded successfully"},
            status_code=200
        )
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occured"
        )