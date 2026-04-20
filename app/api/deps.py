from app.core.database import SessionLocal
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.security import oauth2_bearer
from jose import JWTError, jwt
from app.core.config import settings
from app.models.auth import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependancy = Annotated[Session,Depends(get_db)]
oauth2_dependancy = Annotated[str,Depends(oauth2_bearer)]

def get_current_user(
    token: oauth2_dependancy,
    db: db_dependancy
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user