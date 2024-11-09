# import module
from fastapi import File, UploadFile, HTTPException

# define a list of file type that is accepted
from CONSTANT import ALLOWED_FILE_TYPES


def validate_filetype(file: UploadFile):
    # get the type of the file and make it lower case for comparision
    file_type = file.content_type.lower()

    # check if the file type is allowed
    if file_type not in ALLOWED_FILE_TYPES:
        # file type is not allowd, so reject it
        raise HTTPException(
            status_code=400,
            detail={"message":"Invalid file type. Only PDF, DOC, and DOCX files are allowed."}
        )