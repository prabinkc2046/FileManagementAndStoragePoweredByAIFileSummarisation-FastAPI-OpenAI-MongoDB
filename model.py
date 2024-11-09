from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId
from datetime import datetime
from uuid import UUID, uuid4

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

#  pydantic modal for User
class User(BaseModel):
    user_id:str
    username: str
    email: str
    hashed_password: str
    disabled: Optional[bool] = None

# define the model for user registration
# this model is required to validate incoming data
class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str  = Field(..., min_length=6)
    email: EmailStr


# Pydantic model for the files collection
class FileModel(BaseModel):
    file_id: str
    name:str
    summary: str
    date_uploaded: datetime
    category: str

# Pydantic model for the storage collection
class StorageModel(BaseModel):
    file_id: str
    is_remote: bool
    file_path: str

# Pydantic model for secret collection
class SecretModel(BaseModel):
    user_id:str
    open_api_key:Optional[str] = None
    remote_user:Optional[str] = None
    remote_host:Optional[str] = None
    ssh_password:Optional[str] = None
    ssh_key_path:Optional[str] = None
    password_key:Optional[str] = None
    saving_on_separate_remote_storage: bool

    
