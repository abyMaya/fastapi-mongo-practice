# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv
from app.models import CalenderEvent, Category, Chat,  CollectionList, CustomCategoryName, CustomCharacterName, CustomItem, CustomSeriesName, Image, Item, Message, SeriesCharacter, Series, User, Character, UserItem, UserSpecificData # モデルをインポート

load_dotenv()  # 環境変数をロード

async def init_db():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    database = client.get_default_database()

    # Beanieの初期化
    await init_beanie(database, document_models=[CalenderEvent, Category, Chat,  CollectionList, CustomCategoryName, CustomCharacterName, CustomItem, CustomSeriesName, Image, Item, Message, SeriesCharacter, Series, User, Character, UserItem, UserSpecificData])  # ここに必要なモデルを追加