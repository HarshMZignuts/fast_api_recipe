from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from app.core.config import settings
from uuid import UUID

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



def create_access_token(user_name:str,user_id:UUID,expires_delta:timedelta):

    encode = {'sub': user_name, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

