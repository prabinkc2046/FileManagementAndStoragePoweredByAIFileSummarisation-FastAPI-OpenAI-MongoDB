# import extracting library
import PyPDF2
import pdfplumber
from docx import Document
from io import BytesIO
from fastapi import UploadFile

# import allowed file types from CONSTANT
from CONSTANT import ALLOWED_FILE_TYPES


async def extract_text_from_pdf(file: UploadFile, words_count):
    # get the file content 
    file_content = BytesIO(await file.read())

    # initialise the empty text
    text = ""

    with pdfplumber.open(path_or_fp=file_content) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text = extracted_text + text
                    if len(text.split()) >= words_count:
                        break
    return " ".join(text.split()[:words_count])


async def extract_text_from_document(file: UploadFile, words_count):
     # get the file content 
    file_content = BytesIO(await file.read())

    # initialise the empty text
    text = ""

    doc = Document(docx=file_content)
    for para in doc.paragraphs:
        extracted_text = para.text
        if extracted_text:
            text = extracted_text + text
            if len(text.split()) >= words_count:
                break
    return " ".join(text.split()[:words_count])



