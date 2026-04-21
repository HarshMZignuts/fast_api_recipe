from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.exceptions import custom_http_exception_handler,validation_exception_handler
from fastapi.exceptions import HTTPException, RequestValidationError
from app.models import auth, recipe
from app.core.database import engine, Base
from fastapi_pagination import  add_pagination



app = FastAPI()
add_pagination(app)
Base.metadata.create_all(bind=engine)
app.include_router(api_router, prefix="/api/v1")
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)