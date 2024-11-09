# import important module
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from datetime import timedelta

# module required for /token 
from user import get_user, verify_password, generate_token, get_current_user, get_current_active_user
from CONSTANT import JWT
from model import Token

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # get the user
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    # verify password
    isVerified = verify_password(password, user['hashed_password'])
   
    if not isVerified:
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )
    
    token = generate_token(data={"username": username}, expire_timedelta=timedelta(minutes=JWT.ACCESS_TOKEN_EXPIRES_MINUTES))
    print(token)
    return {"access_token": token, "token_type": "bearer"}
