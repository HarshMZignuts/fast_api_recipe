from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from typing import List
from datetime import datetime

class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(default=None,min_length=3, max_length=300)
    ingredients: List[str]
    instructions: str
    cooking_time: int | None = Field(default=None, gt=0)
    servings: int | None = Field(default=None, gt=0)


class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    id: UUID
    user_id: UUID
    created_at: datetime  
    updated_at: datetime | None  

    class Config:
        from_attributes = True

class RecipeUpdate(BaseModel):
    title: str | None = Field(default=None,min_length=3, max_length=100)
    description: str | None = Field(default=None,min_length=3, max_length=300)
    ingredients: List[str] | None = Field(default=None)
    instructions: str | None = Field(default=None,min_length=3, max_length=1000)
    cooking_time: int | None = Field(default=None, gt=0)
    servings: int | None = Field(default=None, gt=0)

