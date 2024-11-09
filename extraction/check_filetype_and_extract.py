# import necessary module
from fastapi import UploadFile
from CONSTANT import ALLOWED_FILE_TYPES
from extraction.extract_text import extract_text_from_document, extract_text_from_pdf
from dotenv import load_dotenv

# load environment variable



# this function checks the type of file
# when the type of file is matched
# use suitable function to extract text
async def check_filetype_and_extract(file: UploadFile, words_count):

    # get the file type
    file_type = ALLOWED_FILE_TYPES[file.content_type.lower()]

    # initialise the return empty text
    text = ""

    # Check if the allowed file type is pdf
    if file_type == "pdf":
        # extract text from the pdf
        text = await extract_text_from_pdf(file, words_count)
    elif file_type in ["doc", "docx"]:
        # extract text from document
        text = await extract_text_from_document(file, words_count)

    return text

    