from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from typing import List
from datetime import datetime

class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    ingredients: List[str]
    instructions: str
    cooking_time: Optional[int] = None
    servings: Optional[int] = None


class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    id: UUID
    user_id: UUID
    created_at: datetime  
    updated_at: datetime | None  

    class Config:
        from_attributes = True