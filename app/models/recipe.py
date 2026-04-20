from sqlalchemy import Column, Integer, String,Boolean, Text,ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class Recipe(Base):
   __tablename__ = "recipes"
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
   title = Column(String,nullable=False)
   description = Column(Text,nullable=True)
   ingredients = Column(Text, nullable=False)
   instructions = Column(Text, nullable=False)
   cooking_time = Column(Integer, nullable=True)
   servings = Column(Integer, nullable=True)
   user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())