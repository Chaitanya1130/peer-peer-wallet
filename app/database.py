from motor.motor_asyncio import AsyncIOMotorClient  # Import from motor
from typing import Dict, Any, Optional, List
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set. Ensure it's defined in Railway variables or a .env file.")

if not DB_NAME:
    raise ValueError("DB_NAME environment variable not set. Ensure it's defined in Railway variables or a .env file.")
    DB_NAME = "walletApp"

client = AsyncIOMotorClient(MONGO_URI) 
db = client[DB_NAME]
user_collection = db["users"]  
transaction_collection = db["transactions"]
wallet_collection = db["wallets"]


async def getUserID(user_id: str):  
    if not ObjectId.is_valid(user_id):
        return None
    return await user_collection.find_one({"_id": ObjectId(user_id)})


async def getuserByusername(username: str):  # Keep these async
    if not username:
        return None
    return await user_collection.find_one({"username": username})


async def getuserByemail(email: str):  # Keep these async
    if not email:
        return None
    return await user_collection.find_one({"email": email})


async def getBalanceByusername(username: str):  # Keep these async
    if not username:
        return None
    currUser = await user_collection.find_one({"username": username})  # Await here
    if not currUser:
        return None
    wallet = await wallet_collection.find_one({"_id": currUser["wallet_id"]})  # Await here
    if not wallet:
        return None
    return wallet["balance"]