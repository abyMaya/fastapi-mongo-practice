from datetime import date, datetime
from typing import List, Optional
import uuid
from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, validator

# PydanticがObjectId型を受け入れるようにする
# class BaseModelWithConfig(BaseModel):
#     class Config:
#         arbitrary_types_allowed = True # 任意の型を許可
#         json_encoders = {
#             ObjectId: str  # ObjectIdを文字列に変換する設定
#         }

class DocumentWithConfig(Document):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# usersコレクション
class User(DocumentWithConfig):
    id: uuid.UUID = uuid.uuid4()
    user_name: str = Indexed(unique=True) # unique
    email: str = Indexed(unique=True)
    password: str
    bg_image_id: Optional[ObjectId] = None
    lists: Optional[List["CollectionList"]] = []

    @property
    def id_str(self):
        return str(self.id) # UUIDを文字列に変換
    
    class Config:
        collection = "users"  # MongoDBのコレクション名

class CollectionList(DocumentWithConfig):    # list_id: ObjectId
    _id: ObjectId
    list_name: str = Indexed(unique=True, fields=["user_id"]) # user_idと組み合わせてユニークに
    created_at: Optional[datetime] = None
    list_items: Optional[List[ObjectId]] = []  # item_idのリスト

    class Config:
        collection = "users"  


# # itemsコレクション
class Item(DocumentWithConfig):
    _id: ObjectId
    item_images: Optional[List[ObjectId]] = [] # image_idのリスト
    item_name: str = Indexed(unique=True)
    item_series: Optional[List[ObjectId]] = [] # series_idのリスト
    item_characters: Optional[List[ObjectId]] = [] # character_idのリスト
    category: Optional[ObjectId] = None # category_id
    tags: Optional[list[str]] = []
    jan_code: Optional[str] = None
    release_date: Optional[datetime] = None
    retailer: Optional[List[str]] = []

    class Config:
        collection = "items" 


# categoriesコレクション
class Category(DocumentWithConfig):
    category_name: str = Indexed(unique=True) # 共有グッズジャンル名

    class Config:
        collection = "categories"


# # seriesコレクション
class Series(DocumentWithConfig):
    series_name: str = Indexed(unique=True)

    class Config:
        collection = "series"


# charactersコレクション
class Character(DocumentWithConfig):
    character_name: str = Indexed(unique=True)

    class Config:
        collection = "characters"


# series_charactersコレクション
class SeriesCharacter(DocumentWithConfig):
    _id: ObjectId
    series_id: ObjectId
    character_id: ObjectId

    class Config:
        collection = "series_characters"

# users_chatsコレクション
class UserItem(DocumentWithConfig):
    _id: ObjectId
    user_id: uuid.UUID
    item_id: ObjectId

    class Config:
        collection = "users_items"

# chatコレクション
class Chat(DocumentWithConfig):
    _id: ObjectId
    chat_name: str = Indexed(unique=True)
    participants: List[uuid.UUID] # user_idのリスト
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    messages: Optional[List["Message"]] = []

    class Config:
        collection = "chats"

class Message(DocumentWithConfig):
    _id: ObjectId
    user_id: uuid.UUID # user_id
    content: str
    timestamp: Optional[datetime]    

    class Config:
        collection = "messages"

# users_chatsコレクション
class UserChat(DocumentWithConfig):
    _id: ObjectId
    user_id: uuid.UUID
    chat_id: ObjectId

    class Config:
        collection = "users_chats"

# imagesコレクション
class Image(DocumentWithConfig):
    _id: ObjectId
    user_id: uuid.UUID # user_id
    item_id: Optional[ObjectId]
    image_url: str
    created_at: Optional[datetime]
    is_background: bool = False
   
    class Config:
        collection = "images"

# eventsコレクション
class Event(DocumentWithConfig):
    _id: ObjectId
    event_name: str
    event_details: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    created_by: uuid.UUID # user_id
    created_at: datetime
    updated_at: Optional[datetime]
    related_series: Optional[List[ObjectId]]# series_id
    related_characters: Optional[List[ObjectId]] # character_id

    class Config:
        collection = "events"

# user_specific_dataコレクション
class UserSpecificData(DocumentWithConfig):
    _id: ObjectId
    user_id: uuid.UUID
    custom_items: Optional[List["CustomItem"]]
    custom_category_names: Optional[List["CustomCategoryName"]]
    custom_series_names: Optional[List["CustomSeriesName"]]
    custom_character_names: Optional[List["CustomCharacterName"]] 

    class Config:
        collection = "user_specific_data"

class CustomItem(DocumentWithConfig):
    _id: ObjectId
    item_id: ObjectId
    custom_images: Optional[List[ObjectId]] # image_id
    custom_item_name: Optional[str]
    custom_series_names: Optional[List[str]] # custom_series_name
    custom_character_names: Optional[List[str]] # custom_character_name
    custom_tags: Optional[List[str]] #tag
    custom_retailer: Optional[str]
    notes: Optional[str]
    created_at: datetime
    exchange_status: Optional[bool] = None
    own_status: Optional[bool] = None

    class Config:
        collection = "custom_items"

class CustomCategoryName(DocumentWithConfig):
    _id: ObjectId
    category_id: ObjectId
    custom_category_name: str

    class Config:
        collection = "custom_categories"

class CustomSeriesName(DocumentWithConfig):
    _id: ObjectId
    series_id: ObjectId
    custom_series_name: str

    class Config:
        collection = "custom_series_names"

class CustomCharacterName(DocumentWithConfig):
    _id: ObjectId
    character_id: ObjectId
    custom_character_name: str

    class Config:
        collection = "custom_character_names"


class UserItem(DocumentWithConfig):
    _id: ObjectId
    user_id: uuid.UUID
    item_id: ObjectId

    class Config:
        collection = "users_items"


class CalenderEvent(DocumentWithConfig):
    _id: ObjectId
    event_name: str
    event_details: str
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    single_date: Optional[date]
    created_by: uuid.UUID # user_id
    created_at: datetime
    updated_at: Optional[datetime]
    related_series: Optional[List[ObjectId]] # series_id
    related_characters: Optional[List[ObjectId]] # character_Id

    class Config:
        collection = "calender_events"


