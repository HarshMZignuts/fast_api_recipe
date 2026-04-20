from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate
from app.core.config import settings
from app.core.security import bcrypt_context
from uuid import UUID
import json

def add_recipe_db(db: Session, recipe_request:RecipeCreate,user_id:UUID):
    db_recipe = Recipe(
        title= recipe_request.title,
        description=recipe_request.description,
        ingredients=json.dumps(recipe_request.ingredients),
        instructions=recipe_request.instructions,
        cooking_time=recipe_request.cooking_time,
        servings=recipe_request.servings,
        user_id=user_id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_all_recipes_db(db: Session):
    return db.query(Recipe).all()