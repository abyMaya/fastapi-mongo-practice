# app/database/config.py
from beanie import init_beanie
from app.models import (
    CalenderEvent, Category, Chat, CollectionList,
    CustomCategoryName, CustomCharacterName, CustomItem,
    CustomSeriesName, Image, Item, Message,
    SeriesCharacter, Series, User, Character,
    UserItem, UserSpecificData
)

async def init_schema(database):
    # Beanieの初期化
    await init_beanie(database, document_models=[
        CalenderEvent, Category, Chat, CollectionList,
        CustomCategoryName, CustomCharacterName, CustomItem,
        CustomSeriesName, Image, Item, Message,
        SeriesCharacter, Series, User, Character,
        UserItem, UserSpecificData
    ])