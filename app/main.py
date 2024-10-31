# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.database.db_connection import Database
from app.init_schema import init_schema
from app.models import Category, Item, Series, User, Character
from pydantic import BaseModel
from app.api.user import router as user_router  # ユーザー用のルーターをインポート
from app.api.item import router as item_router  # アイテム用のルーターをインポート


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database()
    database = await db.connect()     
    await init_schema(database) # データベースのスキーマを初期化
    yield  # アプリケーションが実行中の間はこの状態を保持

app = FastAPI(lifespan=lifespan)

# ルーターを追加
app.include_router(user_router)  # ユーザー関連のルーターを追加
app.include_router(item_router)  # アイテム関連のルーターを追加