from sqlalchemy.orm import Session
from app.models.auth import User
from app.schemas.auth import UserCreate
from app.core.config import settings
from app.core.security import bcrypt_context

def create_user_db(db: Session, user: UserCreate):
    db_user = User(
        user_name=user.user_name,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_code=user.phone_code,
        phone_number=user.phone_number,
        email=user.email,
        hashed_password=bcrypt_context.hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()