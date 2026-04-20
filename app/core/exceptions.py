from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.schemas.response import APIResponse

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content= APIResponse(
            is_error= True,
            status= exc.status_code,
            message=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
            data= None
        ).model_dump() 
    )

from fastapi.exceptions import RequestValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    cleaned_errors = []

    for err in exc.errors():
        err_copy = err.copy()

        # remove or convert non-serializable objects
        if "ctx" in err_copy:
            err_copy["ctx"] = {
                k: str(v) for k, v in err_copy["ctx"].items()
            }

        cleaned_errors.append(err_copy)

    return JSONResponse(
        status_code=422,
        content= APIResponse(
            is_error= True,
            status= 422,
            message= "Validation error",
            data= cleaned_errors
        ).model_dump() 

    )