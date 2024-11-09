# import important module
from fastapi import File, UploadFile, FastAPI, HTTPException, Query, Depends

# module required for /token 
from user import get_user, verify_password, generate_token, get_current_user, get_current_active_user

# import module required for /extract 
from extraction.validate_filetype import validate_filetype
from extraction.check_filetype_and_extract import check_filetype_and_extract

async def extract_text(
    words: int,
    file: UploadFile = File(...),
    # default value of the words count will be passed from main.py
    current_active_user: dict = Depends(get_current_active_user)
):
    
    # check the validity of the file type
    # throws error if the filetype is not pdf or doc or docx
    validate_filetype(file)

    # extract the text from the matching file type
    text = await check_filetype_and_extract(file, words)

    return {"text": text}