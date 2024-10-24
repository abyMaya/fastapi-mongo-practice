# app/init.py
from datetime import datetime
import os
import uuid
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import CalenderEvent, Category, Chat,  CollectionList, CustomCategoryName, CustomCharacterName, CustomItem, CustomSeriesName, Image, Item, Message, SeriesCharacter, Series, User, Character, UserItem, UserSpecificData
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def init_schema():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    database = client.get_default_database()

    await init_beanie(database, document_models=[CalenderEvent, Category, Chat,  CollectionList, CustomCategoryName, CustomCharacterName, CustomItem, CustomSeriesName, Image, Item, Message, SeriesCharacter, Series, User, Character, UserItem, UserSpecificData])

    # 初期データを挿入
    # ユーザーを取得
    test_user = await User.find_one({"user_name": "test_user"})  # ユーザーを探す

    if not test_user:  # ユーザーが存在しない場合
        test_user = User(
            user_id=uuid.uuid4(),
            user_name="test_user",
            email="test@example.com",
            password="hashed_password"
        )

        await test_user.insert()  # データベースにユーザーを追加

        # ユーザー独自データを作成
        user_specific_data = UserSpecificData(
            _id=ObjectId(),
            user_id=test_user.id,
            custom_items=[
                CustomItem(
                    _id=ObjectId(),
                    item_id=ObjectId("60d5f484a2d21a1d4cf1b0e2"),
                    custom_images=[],
                    custom_item_name="My Test Custom Item",
                    custom_series_names=["My Test Series"],
                    custom_character_names=["My Test Character"],
                    custom_tags=["tag1", "tag2"],
                    custom_retailer="My Test Local Store",
                    notes="This is a personal note.",
                    created_at=datetime.now(),
                    exchange_status=False,
                    own_status=True
                )
            ],
            custom_category_names=[
                CustomCategoryName(
                    _id=ObjectId(),
                    category_id=ObjectId("60d5f484a2d21a1d4cf1b0e3"),
                    custom_category_name="My Test Custom Category"
                )
            ],
            custom_series_names=[
                CustomSeriesName(
                    _id=ObjectId(),
                    series_id=ObjectId("60d5f484a2d21a1d4cf1b0e4"),
                    custom_series_name="My Test Custom Series"
                )
            ],
            custom_character_names=[
                CustomCharacterName(
                    _id=ObjectId(),
                    character_id=ObjectId("60d5f484a2d21a1d4cf1b0e5"),
                    custom_character_name="My Test Custom Character"
                )
            ]
        )
        # ユーザー独自データをデータベースに追加
        try:
            await user_specific_data.insert()  # ユーザー独自データをデータベースに追加
        except Exception as e:
            print(f"Error inserting user_specific_data: {e}")  # エラー内容を表示
 
    if not await User.find_one({"lists": {"$elemMatch": {"list_name": "Test Collection"}}}): # コレクションリストが存在しない場合

        # コレクションリストを作成
        collection_list = CollectionList(
            _id=ObjectId(), # リストIDを自動生成
            list_name="Test Collection",
            created_at=datetime.now(),
            list_items=[ObjectId("67179fe7e405ba2805aebca2")]         
        )
        await collection_list.insert() # コレクションリストをデータベースに追加
        # 作成したコレクションリストをユーザーのリストに追加
        test_user.lists.append(collection_list) # コレクションリストを追加
        await test_user.save() # 更新されたユーザーを再度保存


    if not await Item.find_one({"item_name": "Test Item"}):  # Test Itemという名前のアイテムが存在しない場合
        # アイテムを作成
        test_item = Item(
            item_name="Test Item"
        )
        await test_item.insert()  # データベースにアイテムを追加

    if not await Category.find_one({"category_name": "Test Category"}):  #  Test Categoryという名前のグッズジャンルが存在しない場合
        # グッズジャンルを作成
        test_category = Category(
            category_name="Test Category"
        )
        await test_category.insert()  # データベースにグッズジャンルを追加

    if not await Series.find_one({"series_name": "Test Series"}):  # Test Seriesという名前の作品名が存在しない場合
        # 作品名を作成
        test_series = Series(
            series_name="Test Series"
        )
        await test_series.insert()  # データベースに作品名を追加

    if not await Character.find_one({"character_name": "Test Character"}):  # Test Characterという名前のキャラクターが存在しない場合
        # キャラクターを作成
        test_character = Character(
            character_name="Test Character"
        )
        await test_character.insert()  # データベースにキャラクターを追加

    if not await SeriesCharacter.find_one({"series_id": ObjectId("60d5f484a2d21a1d4cf1b0e1")}):  # Ttestseriescharacter1という作品IDが存在しない場合
        # 作品キャラクターを作成
        test_series_characters = SeriesCharacter(
            series_id=ObjectId("60d5f484a2d21a1d4cf1b0e1"),  # ObjectIdで初期化
            character_id=ObjectId("60d5f484a2d21a1d4cf1b0e2")  # ObjectIdで初期化
        )
        await test_series_characters.insert()  # データベースに作品キャラクターを追加


    if not await Chat.find_one({"chat_name": "test_chat"}):  
        test_chat = Chat(
            _id=ObjectId(),  
            chat_name="test_chat", 
            participants=[uuid.UUID("123e4567-e89b-12d3-a456-426614174000"), uuid.UUID("550e8400-e29b-41d4-a716-446655440000")],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            messages=[]  # 最初は空のメッセージリスト
        )
        await test_chat.insert()  # チャットをデータベースに追加

        # メッセージの追加処理
        message = Message(
            _id=ObjectId(), 
            user_id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),  
            content="Welcome!!",
            timestamp=datetime.now()
        )
        await message.insert()  # メッセージをデータベースに追加
        test_chat.messages.append(message)  # チャットにメッセージを追加
        await test_chat.save()  # 更新されたチャットを保存


    if not await UserItem.find_one({"item_id": ObjectId("61f5f484a2d21a1d4cf1b0e6")}): 

        test_users_items = UserItem(
            user_id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
            item_id=ObjectId("61f5f484a2d21a1d4cf1b0e6") 
        )
        await test_users_items.insert() 
 
    test_image = await Image.find_one({"image_url": "https://example.com/images/image1.jpg"}) 

    if not test_image: 
        test_image = Image(
            _id=ObjectId(), 
            user_id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"), 
            item_id=ObjectId("67179fe7e405ba2805aebca2"), 
            image_url="https://example.com/images/image1.jpg", 
            created_at=datetime.now(), 
            is_background=False 
        )
    try:
        await test_image.insert()  # 画像をデータベースに挿入
    except Exception as e:
        print(f"Error inserting image: {e}")  # エラー内容を表示


    # イベントが存在しない場合に新しいイベントを作成
    if not await CalenderEvent.find_one({"event_name": "Test Event"}):  
        test_calender_event = CalenderEvent(
            _id=ObjectId(),  # 新しいObjectIdを生成
            event_name="Test Event",
            event_details="This is a test event for demonstration.",
            start_datetime=datetime(2024, 11, 25, 10, 0),  # 開始日時を設定
            end_datetime=datetime(2024, 11, 30, 23, 59),  # 終了日時を設定
            single_date=None,  # 特定の日付が必要ない場合はNone
            created_by=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),  # ユーザーIDをUUIDとして設定
            created_at=datetime.now(),  # 登録日時を設定
            updated_at=datetime.now(),  # 更新日時を設定
            related_series=[ObjectId("60d5f484a2d21a1d4cf1b0e4")],  # 作品IDのリスト
            related_characters=[ObjectId("60d5f484a2d21a1d4cf1b0e5")]  # キャラクターIDのリスト
        )
        # イベントをデータベースに追加
        await test_calender_event.insert()

if __name__ == "__main__":
    asyncio.run(init_schema())