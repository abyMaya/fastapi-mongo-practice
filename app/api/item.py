# app/api/item.py
from datetime import date
from typing import List
from bson import ObjectId
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from app.database.db_item import create_item
from app.models import Category, Character, Item, Series, User
from app.database.db_user import create_user, get_user

# PydanticがObjectId型を受け入れるようにする
class BaseModelWithConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True # 任意の型を許可
        json_encoders = {
            ObjectId: str # ObjectIdを文字列に変換する設定
        }

app = FastAPI
router = APIRouter()

class ItemRequest(BaseModelWithConfig): 
     
    item_images: List[str]
    item_name: str
    item_series: str
    item_character: str
    category: str
    tags: List[str]
    jan_code: str
    release_date: date
    retailer: List[str]

    @field_validator('item_images')
    def validate_item_images(cls, v):
        return [ObjectId(i) if isinstance(i, str) else i for i in v]

    @field_validator('item_series', 'item_character', 'category')
    def validate_object_id(cls, v):
        return ObjectId(v) if isinstance(v, str) else v

@router.post("/api/items")
async def create_item_endpoint(item_request: ItemRequest):

    item = Item(**item_request.model_dump())
    created_item = await create_item(item)
    return created_item

    # # model_dump した辞書を受け取って一旦変数に格納
    # item_data = item_request.model_dump()

    # # 必要なフィールドを ObjectId に変換
    # item_data["item_images"] = [ObjectId(image_id) for image_id in item_data["item_images"]]
    # item_data["item_series"] = ObjectId(item_data["item_series"])
    # item_data["item_character"] = ObjectId(item_data["item_character"])
    # item_data["category"] = ObjectId(item_data["category"])

    # # 変換後のデータを使って Item をインスタンス化
    # item = Item(**item_data)    

    # # アイテムの作成処理
    # created_item = await create_item(item)
    # return created_item