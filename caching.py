#Import third party library
from fastapi import Depends
from cachetools import TTLCache

# Import local application module
from user import get_current_active_user
from secret.retrieve_secret import retrieve_secret

# Create a cache with a time to live to refresh after certain period
secret_info_cache = TTLCache(maxsize=100.0, ttl=3)

# async def get_secret_info(current_active_user: dict = Depends(get_current_active_user)):
#     user_id = current_active_user.get("user_id")

#     if user_id in secret_info_cache:
#         return secret_info_cache[user_id]
    
#     secret_info = await retrieve_secret(current_active_user)
#     secret_info_cache[user_id] = secret_info
#     print("running cache", secret_info)
#     return secret_info

async def get_secret_info(current_active_user: dict = Depends(get_current_active_user)):
    user_id = current_active_user.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if user_id in secret_info_cache:
        print("Cache hit:", secret_info_cache[user_id])
        return secret_info_cache[user_id]
    
    secret_info = await retrieve_secret(current_active_user)
    secret_info_cache[user_id] = secret_info
    print("Cache miss, retrieved secret:", secret_info)
    return secret_info
