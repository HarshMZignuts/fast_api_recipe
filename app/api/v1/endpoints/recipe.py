
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.response import APIResponse
from app.api.deps import get_db, get_current_user
from typing import Annotated
from starlette import status
from app.schemas.recipe import RecipeCreate,RecipeResponse,RecipeUpdate
from app.crud.recipe import add_recipe_db,get_all_recipes_db,get_recipe_by_recipe_id_db,update_recipe_db,soft_delete_recipe_db
from uuid import UUID
from app.models.auth import User
import json

router = APIRouter()

db_dependancy = Annotated[Session,Depends(get_db)]
current_user_dependancy = Annotated[User,Depends(get_current_user)]

@router.post("/add-recipe",status_code=status.HTTP_201_CREATED)
async def add_recipe(recipe_request: RecipeCreate, db: db_dependancy,current_user:current_user_dependancy):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failed')
    
    recipe = add_recipe_db(db=db,recipe_request=recipe_request,user_id=current_user.id)

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Recipe is not created')
    
    return APIResponse(
        is_error=False,
        status= 201,
        message="Recipe added successfully",
        data=RecipeResponse(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            ingredients=json.loads(recipe.ingredients),
            instructions=recipe.instructions,
            cooking_time=recipe.cooking_time,
            servings=recipe.servings,
            user_id=recipe.user_id,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at            
        )
    )

@router.get("/get-all-recipes",status_code=status.HTTP_200_OK,response_model=APIResponse[list[RecipeResponse]])
async def get_all_recipes(db: db_dependancy,current_user:current_user_dependancy):
     if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failed')

     recipes = get_all_recipes_db(db=db)
     for r in recipes:
        r.ingredients = json.loads(r.ingredients)
     return APIResponse(
        is_error=False,
        status= 200,
        message="Recipe fetch successfully",
        data=recipes
    )

@router.get("/{recipe_id}",status_code=status.HTTP_200_OK,response_model=APIResponse[RecipeResponse])
async def get_recipe(db: db_dependancy,current_user:current_user_dependancy,recipe_id:UUID):
     if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failed')
     
     recipe = get_recipe_by_recipe_id_db(db=db,recipe_id=recipe_id)
     if recipe is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Recipe not found.')
     recipe.ingredients = json.loads(recipe.ingredients)
     return APIResponse(
         is_error=False,
         status=200,
         message="Recipe fetch successfully",
         data=recipe
     )

@router.put("/{recipe_id}",status_code=status.HTTP_200_OK,response_model=APIResponse[RecipeResponse])
async def update_recipe(db: db_dependancy,current_user:current_user_dependancy,recipe_update_request:RecipeUpdate,recipe_id:UUID):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failed')
    recipe = get_recipe_by_recipe_id_db(db=db,recipe_id=recipe_id)
    if recipe is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Recipe not found.')
    not_user_recipe = recipe.user_id != current_user.id
    if not_user_recipe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='This recipe does not belong to you.')
    
    updated_recipe_data = update_recipe_db(db=db,recipe_id=recipe_id,recipe_update_request=recipe_update_request)
    if updated_recipe_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Recipe not updated.')
    updated_recipe_data.ingredients = json.loads(updated_recipe_data.ingredients)
    return APIResponse(
         is_error=False,
         status=200,
         message="Recipe update successfully",
         data=updated_recipe_data
     )


@router.delete("/{recipe_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def delete_recipe(db:db_dependancy,current_user:current_user_dependancy,recipe_id:UUID):
    recipe = get_recipe_by_recipe_id_db(db=db,recipe_id=recipe_id)
    if recipe is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Recipe not found.')
    not_user_recipe = recipe.user_id != current_user.id
    if not_user_recipe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='This recipe does not belong to you, you can\'t delete it.')
    
    delete_recipe_data = soft_delete_recipe_db(db=db,recipe_id=recipe_id)

    if delete_recipe_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Recipe not deleted.')
    return APIResponse(
         is_error=False,
         status=200,
         message="Recipe delete successfully",
         data=None
     )

    



    

    


