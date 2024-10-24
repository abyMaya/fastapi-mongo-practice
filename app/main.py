# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.init_schema import init_db, init_schema
from app.models import Category, Item, Series, User, Character
from pydantic import BaseModel
from app.api.user import router as user_router  # ユーザー用のルーターをインポート

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_schema()

# ルーターを追加
app.include_router(user_router)  # プレフィックスなしのユーザーエンドポイント
