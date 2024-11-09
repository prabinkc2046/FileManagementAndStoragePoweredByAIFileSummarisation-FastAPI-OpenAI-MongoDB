# module
from uuid import uuid4

# Fastapi module
from fastapi import HTTPException
from  fastapi.responses import JSONResponse

# module for mongodb connection
from mongodb.mongodb import users_collection

# module required for /register 
from model import User, UserRegistration
from user import get_password_hash

async def register_user(user: UserRegistration):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    # validate email format
    if not user.email or "@" not in user.email:
        raise HTTPException(status_code=400, detail="Invalid email format")

    hashed_password = get_password_hash(user.password)

    # Create unique user id
    user_id = str(uuid4())

    # create a user document 
    user_document = User(
        user_id=user_id,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        disabled=False
    )

    users_collection.insert_one(user_document.model_dump())
    return JSONResponse(
        content={"message":"User registered successfully"},
        status_code=200
    )
