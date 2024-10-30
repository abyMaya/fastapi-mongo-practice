#app/database/db_user.py
from pydantic import BaseModel
from app.database.db_connection import Database
from app.models import User

db = Database()

async def create_user(user: User):
    await db.connect()
    await user.insert()
    return user

async def get_user(user_id: str):
    await db.connect()
    user = await User.get(user_id)
    return user