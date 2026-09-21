from fastapi import Request
from fastapi.responses import JSONResponse
from .app_exception import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message},
    )


async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Validation failed", "errors": exc.errors()},
    )
