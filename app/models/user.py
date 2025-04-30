from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    username:str
    email:str

class UserCreate(User):
    password:str
class UserInDB(User):
    hash_pass:str
    balance: Optional[float] = None  
    id:Optional[str]