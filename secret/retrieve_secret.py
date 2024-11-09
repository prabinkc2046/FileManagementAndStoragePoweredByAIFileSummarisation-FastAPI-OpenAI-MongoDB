from fastapi import status, HTTPException
from mongodb.mongodb import secret_collection
from typing import Dict, Optional, List

# Function to retrive secret from database
async def retrieve_secret(current_active_user: dict, fields: Optional[List[str]] = None) -> Dict[str, Optional[str]]:
    # Get the user_id of the active user
    active_user_id = current_active_user.get("user_id")

    if active_user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Build the query and projection
    query = {"user_id": active_user_id}
    projection = {field: 1 for field in fields} if fields else None

    # Retrieve the secret information from the database
    secret_info = secret_collection.find_one(query, projection=projection)

    if secret_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    # Return the secret information
    return secret_info
