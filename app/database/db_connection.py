# app/database/db_connection.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

class Database:
    def __init__(self):
        self.client = None # MongoDBクライアント
        self.database = None # デフォルトのデータベース

    async def connect(self):
        load_dotenv()  # 環境変数をロード
        self.client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
        self.database = self.client.get_default_database()
        return self.database

    async def disconnect(self):
        if self.client:
            self.client.close()