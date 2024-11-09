from fastapi import File, UploadFile, FastAPI, HTTPException, Query, Depends
from jose import JWTError, jwt
from  datetime import timedelta

# module required for /refresh
from  model import TokenData
from context import oauth_scheme
from CONSTANT import JWT
from user import get_user, generate_token

# module for mongodb connection
from mongodb.mongodb import users_collection, blacklist_collection

async def refresh_token(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(token=token, key=JWT.SECRET_KEY, algorithms=[JWT.ALGORITHM])
        jti = decoded_token.get("jti")
        if jti is None or blacklist_collection.find_one({"jti": jti}):
            raise credentials_exception
        username: str = decoded_token.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    # create a new token with a new expiration time
    access_token_expires = timedelta(minutes=JWT.ACCESS_TOKEN_EXPIRES_MINUTES)
    new_token = generate_token(data={"username": username}, expire_timedelta=access_token_expires)
    return {"access_token": new_token, "token_type": "bearer"}
