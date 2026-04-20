from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, UserResponse
from app.schemas.response import APIResponse
from app.api.deps import get_db
from typing import Annotated
from starlette import status
from app.models.auth import User
from app.crud.auth import create_user_db

router = APIRouter()

db_dependancy = Annotated[Session,Depends(get_db)]

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




    
    