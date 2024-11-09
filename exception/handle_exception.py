from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

async def validation_exception_handle(request: Request, exc: RequestValidationError):
    erros = exc.errors()
    formatted_errors = []

    for error in erros:
        loc = " -> ".join(str(x) for x in error["loc"])
        formatted_errors.append({
            "field": loc,
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=422,
        content={"detail": formatted_errors}
    )