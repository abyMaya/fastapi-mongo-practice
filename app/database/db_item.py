#app/database/db_item.py
from pydantic import BaseModel
from app.database.db_connection import Database
from app.models import Item, User

db = Database()

async def create_item(item: Item):
    await db.connect()
    print(item)  # 挿入するアイテムの内容を表示
    await item.insert()
    return item



# get_items()
# get_item(item_id: str)
# update_item(item_id: str, update_data: dict)
# delete_item(item_id: str)


# async def create_user(user: User):
#     await db.connect()
#     await user.insert()
#     return user

# async def get_user(user_id: str):
#     await db.connect()
#     user = await User.get(user_id)
#     return user