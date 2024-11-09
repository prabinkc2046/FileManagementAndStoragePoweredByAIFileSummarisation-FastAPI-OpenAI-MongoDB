from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse

from mongodb.mongodb import secret_collection
from user import get_current_active_user


async def get_secret_details(
    current_active_user: dict = Depends(get_current_active_user)
):
    # Get the userid of the current active user
    user_id = current_active_user.get("user_id")

    # If user id is not found, raise an error
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )

    # Fetch current active user's secret details from the database
    secret = secret_collection.find_one({"user_id": user_id}, {"_id": 0})

    # If secret does not exist, raise an error
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secret details not found"
        )

    
    # Prepare the response excluding the ssh_key_path
    response_data = {key: value for key, value in secret.items()}

    # Return the details along with the encoded file
    return JSONResponse(content=response_data)
