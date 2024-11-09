from mongodb.mongodb import users_collection, blacklist_collection
from context import pwd_context, oauth_scheme
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional
from CONSTANT import JWT
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from model import TokenData

# get user from mongo db
def get_user(username:str):
    user = users_collection.find_one({"username":username})
    if not user:
        return False
    return user

# verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# hash the password
def get_password_hash(password):
    return pwd_context.hash(password)

# generate token
def generate_token(data:dict, expire_timedelta:Optional[timedelta] = None):
    jti = str(uuid4())
    to_encode = data.copy()
    if expire_timedelta:
        expire = datetime.utcnow() + expire_timedelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "jti":jti})

    encoded_token = jwt.encode(to_encode,key=JWT.SECRET_KEY, algorithm=JWT.ALGORITHM)
    return encoded_token

# get the current user from the token
def get_current_user(token:str = Depends(oauth_scheme)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        decoded_token = jwt.decode(token=token,key=JWT.SECRET_KEY,algorithms=[JWT.ALGORITHM])
        # get the user
        username = decoded_token.get("username")
        if username is None:
            print("Username not found in token")
            raise credential_exception
        token_data = TokenData(username=username)

        # get the jti from the decoded_token
        jti = decoded_token.get("jti")

        if jti is None:
            raise credential_exception
        
        # check if the token's JTI is in the blacklist
        if blacklist_collection.find_one({"jti": jti}):
            print("Token is revoked")
            raise HTTPException(status_code=401, detail="Token is revoked")
        # get token expire time
        exp = decoded_token.get("exp")
        expire = datetime.fromtimestamp(exp)
        now = datetime.utcnow()
        if now > expire:
            print("Token has expired so it is revoked now")
            blacklist_collection.insert_one({"jti": jti, "revoked_at": datetime.utcnow()})
            raise credential_exception
        
    except JWTError as e:
        print(f"JWT error: {e}")
        raise credential_exception
    user = get_user(token_data.username)
    if user is None:
        print("User not found in database")
        raise credential_exception
    return user


# get the current active user
def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("disabled"):
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return current_user