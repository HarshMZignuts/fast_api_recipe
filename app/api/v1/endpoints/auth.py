from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, UserResponse,UserLoginRequest
from app.schemas.response import APIResponse
from app.api.deps import get_db
from typing import Annotated
from starlette import status
from app.models.auth import User
from app.crud.auth import create_user_db
from app.core.security import bcrypt_context,create_access_token
from datetime import datetime, timedelta, timezone
from app.core.config import settings


router = APIRouter()

db_dependancy = Annotated[Session,Depends(get_db)]


def authenticate_user(user_name:str,password:str,db):
    user = db.query(User).filter(User.user_name == user_name).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user


@router.post("/create-user",status_code=status.HTTP_201_CREATED,response_model=APIResponse)
async def create_user(user:UserCreate,db:db_dependancy):
    existing_user = db.query(User).filter(User.user_name == user.user_name).first()
    existing_phone_number = db.query(User).filter(User.phone_code == user.phone_code).filter(User.phone_number == User.phone_number).first()
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User name already exists")
    if existing_phone_number:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    if existing_email:
        raise HTTPException(status_code=400,detail="Email already exists")
    
    user_model = create_user_db(user=user,db=db)
    if not user_model:
        raise HTTPException(status_code=400, detail="User not created")
    
    return APIResponse(
        status=201,
        message="User created successfully",
        is_error=False,
        data=None
    )


@router.post("/login",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def login(user_request:UserLoginRequest,db:db_dependancy):
    user = authenticate_user(user_request.user_name, user_request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    access_token = create_access_token(
        user_name=user.user_name,
        user_id=str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return APIResponse(
        status=200,
        message="User login successfully.",
        is_error=False,
        data= UserResponse(
            id=user.id,
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_code=user.phone_code,
            phone_number=user.phone_number,
            email=user.email,
            access_token=access_token
        )
    )









    
    