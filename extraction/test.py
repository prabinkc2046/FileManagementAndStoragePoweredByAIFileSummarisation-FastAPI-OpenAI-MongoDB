import httpx
from fastapi import HTTPException
from fastapi.responses import JSONResponse
async def use_summary_api():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/summarise")
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to get summary"
            )
        result = response.json()
        return result["summary"]

result = use_summary_api()
print(result)