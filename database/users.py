from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pymongo import DESCENDING
from bson import ObjectId
import dotenv
import os
from models.users import UserBase



dotenv.load_dotenv()

MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# Replace this with your MongoDB collection name for users
USERS_COLLECTION_NAME = "users"

class UserDB:
    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION_URL)
        self.db = self.client[DATABASE_NAME]
        self.users_collection = self.db.get_collection(USERS_COLLECTION_NAME)

    async def create_user(self, user_data):
        new_user = await self.users_collection.insert_one(user_data)
        new_user_id = str(new_user.inserted_id)
        return new_user_id
    
    def get_all_user(self, id, limit):
        if not id or id == "null":
            users_cursor = self.users_collection.find({}, {"password": False}).sort([("_id", DESCENDING)]).limit(limit) # Find the documents after the given id and get 'limit' number of rows
            users_list = list(users_cursor)
            return users_list
        user = self.users_collection.find_one({"_id": ObjectId(id)}) # Find the document with the given id
        if not user:
            return None
        
        users_cursor = self.users_collection.find({"_id": {"$lt": ObjectId(id)}}).sort([("_id", DESCENDING)]).limit(limit) # Find the documents after the given id and get 'limit' number of rows
        users_list = list(users_cursor)
        return users_list

    async def get_user(self, user_id):
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        return user
    
    async def get_user_email(self, email):
        user = await self.users_collection.find_one({"email": email})
        return user
    