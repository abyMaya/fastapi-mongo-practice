#app/database/db_user.py
from pydantic import BaseModel
from app.database.db_connection import Database
from app.models import User

db = Database()

async def create_user(user: User):
    await db.connect()
    await user.insert()
    return user