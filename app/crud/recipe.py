from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate
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
    return db.query(Recipe).filter(Recipe.is_deleted == False)

def get_recipe_by_recipe_id_db(db:Session,recipe_id:UUID):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id,Recipe.is_deleted == False).first()
    return recipe


def update_recipe_db(db:Session,recipe_id:UUID,recipe_update_request:RecipeUpdate):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe_update_request.title and recipe_update_request.title.strip():
        recipe.title = recipe_update_request.title.strip()
    if recipe_update_request.description and recipe_update_request.description.strip():
        recipe.description = recipe_update_request.description.strip()
    if recipe_update_request.instructions and recipe_update_request.instructions.strip():
         recipe.instructions = recipe_update_request.instructions.strip()
    if recipe_update_request.ingredients:
        recipe.ingredients = json.dumps(recipe_update_request.ingredients)
    if recipe_update_request.cooking_time is not None:
        recipe.cooking_time = recipe_update_request.cooking_time 
    if recipe_update_request.servings is not None:
        recipe.servings = recipe_update_request.servings
    
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def soft_delete_recipe_db(db:Session,recipe_id:UUID):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    recipe.is_deleted = True

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

