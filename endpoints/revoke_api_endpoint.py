from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from datetime import datetime

# module for mongodb connection
from mongodb.mongodb import blacklist_collection

# module required for /revoke
from context import oauth_scheme
from CONSTANT import JWT

async def revoke_token(token: str = Depends(oauth_scheme)):
    try:
        encoded_token = jwt.decode(token=token, key=JWT.SECRET_KEY, algorithms=[JWT.ALGORITHM])
        jti = encoded_token.get("jti")
        if jti is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        # add the token's jti to the blacklist
        blacklist_collection.insert_one({"jti": jti, "revoked_at": datetime.utcnow()})
        return {"message":"Token has been revoked"}
    except JWTError as e:
        raise HTTPException(status_code=400, detail="Invalid token")