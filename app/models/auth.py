from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_name = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_code = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_deleted = Column(Boolean,default=False)

