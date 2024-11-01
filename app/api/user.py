# app/api/user.py
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
from app.models import Category, Character, Item, Series, User
from app.database.db_user import create_user, get_user

app = FastAPI
router = APIRouter()

class UserRequest(BaseModel):
    user_name: str
    email: str
    password: str

@router.post("/signup")
async def signup(user_request: UserRequest):
    user = User(**user_request.model_dump())

    created_user = await create_user(user)
    return created_user

    # await user.insert()
    # return user

@router.get("/login")
async def get_user_endpoint(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# class ItemCreateRequest(BaseModel):
#     item_name: str

# @app.post("/items/")
# async def create_item(item: ItemCreateRequest):
#     item_document = Item(**item.model_dump())
#     await item_document.insert()
#     return item_document

# @app.get("/items/{item_id}")
# async def get_item(item_id: str):
#     item = await Item.get(item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item


# class CategoryCreateRequest(BaseModel):
#     category_name: str

# @app.post("/categories/")
# async def create_category(category: CategoryCreateRequest):
#     category_document = Category(**category.model_dump())
#     await category.insert()
#     return category

# @app.get("/categories/{category_id}")
# async def get_category(category_id: str):
#     category = await Category.get(category_id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return category


# class SeriesCreateRequest(BaseModel):
#     category_name: str

# @app.post("/series/")
# async def create_series(series: SeriesCreateRequest):
#     Series = Series(**series.model_dump())
#     await series.insert()
#     return series

# @app.get("/series/{series_id}")
# async def get_series(series_id: str):
#     series = await Series.get(series_id)
#     if not series:
#         raise HTTPException(status_code=404, detail="Series not found")
#     return series


# class CharactersCreateRequest(BaseModel):
#     character_name: str

# @app.post("/character/")
# async def create_character(character: CharactersCreateRequest):
#     character = Character(**character.model_dump())
#     await character.insert()
#     return character

# @app.get("/character/{character_id}")
# async def get_character(character_id: str):
#     character = await Character.get(character_id)
#     if not character:
#         raise HTTPException(status_code=404, detail="Character not found")
#     return character

