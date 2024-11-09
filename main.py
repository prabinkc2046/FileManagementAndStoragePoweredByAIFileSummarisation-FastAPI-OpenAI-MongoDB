# Standard Library Imports
from typing import Optional

# Third-Party Library Imports
from fastapi import (
    FastAPI, File, UploadFile, Query, Depends, Form, BackgroundTasks, Request
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm

# Local Application Imports

## User and Security
from user import get_current_active_user
from context import oauth_scheme

## Models
from model import Token, UserRegistration

## API Endpoints
from endpoints.extract_api_endpoint import extract_text
from endpoints.token_api_endpoint import login
from endpoints.register_api_endpoint import register_user
from endpoints.revoke_api_endpoint import revoke_token
from endpoints.refresh_api_endpoint import refresh_token
from endpoints.summarise_api_endpoint import get_summary
from endpoints.upload_api_endpoint import get_upload
from endpoints.download_file_api_endpoint import get_download
from endpoints.submit_secret_api_endpoint import get_upload_secret

## Exception Handling
from exception.handle_exception import validation_exception_handle

## Caching
from caching import get_secret_info


# initiate an instance of fastapi 
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your React server's IP and port
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],  
    allow_headers=["*"],  # Specify allowed headers
)


# handle  exception
@app.exception_handler(RequestValidationError)
async def handle_exception(
    request: Request,
    exc: RequestValidationError
):
    return await validation_exception_handle(request, exc)



from fastapi.responses import JSONResponse
from endpoints.get_secret_details_api_endpoint import get_secret_details

@app.get("/secret-details", response_class=JSONResponse)
async def secret_details(
    current_active_user: dict = Depends(get_current_active_user)
):
    return await get_secret_details(
        current_active_user
    )
    


# API ENDPOINT to store the secret information
@app.post("/submit_secret")
async def upload_secret(
    open_api_key: Optional[str] = Form(None),
    remote_user: Optional[str] = Form(None),
    remote_host: Optional[str] = Form(None),
    ssh_password: Optional[str] = Form(None),
    password_key: Optional[str] = Form(None),
    saving_on_separate_remote_storage: bool = Form(...),
    file: UploadFile = File(None),  # File upload
    current_active_user: dict = Depends(get_current_active_user)  
):
    return await get_upload_secret(
        open_api_key,
        remote_user,
        remote_host,
        ssh_password,
        password_key,
        saving_on_separate_remote_storage,
        file,
        current_active_user
    )

#api endpoint to register new user
@app.post("/register")
async def register(new_user: UserRegistration):
    return await register_user(user=new_user)

# Token endpoint
@app.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data)

# define an api end point for extracting text from pdf and doc file only
# Example use of extract endpoint
# http://127.0.0.1:8000/extract?words=23
@app.post("/extract")
async def get_extracted_text(
    words: int,
    file: UploadFile = File(...), 
    current_active_user: dict = Depends(get_current_active_user)
):
    return await extract_text(words, file, current_active_user)


# API endpoint to get summary of the extracted text
# Example use of summarise end point
# http://127.0.0.1:8000/summarise?words=50&max_tokens=25&summary_counts=20
@app.post("/summarise")
async def summarise(
    words: int,
    max_tokens: int,
    summary_counts: int,
    # secret_info:dict = Depends(get_secret_info),
    file: UploadFile = File(...),  
    current_active_user: dict = Depends(get_current_active_user)
):
    return await get_summary(
        words,
        max_tokens,
        summary_counts,
        # secret_info,
        file,
        current_active_user
    )

# API endpoint to upload a file on server or s3
#Example use, saving locally
#http://127.0.0.1:8000/upload?words=100&storage_directory_name=your storage&category=dance and music&max_tokens=25&summary_counts=25
@app.post("/upload")
async def upload(
    words: int, # number of words to be extracted from file
    category: str, # this category will be used to create a folder with this category name
    max_tokens: int, # max token to use for summarising file
    summary_counts: int, # number of words to use in summary
    storage_directory_name:str, # name of the storage directory
    secret_info:dict = Depends(get_secret_info),
    file: UploadFile = File(...),        
    current_active_user: dict = Depends(get_current_active_user)
):
    return await get_upload(
        words,
        category,
        max_tokens,
        summary_counts,
        storage_directory_name,
        secret_info,
        file,
        current_active_user
    )


# End point to download file from remote or local (fast api server)
@app.get("/download/{file_id}")
async def download(
    file_id:str,
    background_task: BackgroundTasks,
    current_active_user: dict = Depends(get_current_active_user),
    secret_info:dict = Depends(get_secret_info)
):
    return await get_download(
        file_id,
        background_task,
        secret_info,
        current_active_user
    )

# API end point to revoke or logout
@app.post("/revoke")
async def get_token_revoked(token: str = Depends(oauth_scheme)):
    return await revoke_token(token)

# API end point to refresh the token
@app.post("/refresh", response_model=Token)
async def get_token_refresh(token: str = Depends(oauth_scheme)):
    return await refresh_token(token)

# run the script as a main program
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
