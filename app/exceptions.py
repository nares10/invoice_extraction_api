from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette import status


async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        detail = exc.detail
        if isinstance(detail, dict):
            payload = detail
        else:
            payload = {"error_code": "HTTP_ERROR", "message": str(detail)}

        return JSONResponse(status_code=exc.status_code, content=payload)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Unexpected server error"
        }
    )
