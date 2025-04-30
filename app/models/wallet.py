from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class Wallet(BaseModel):
    balance :float=0.0

class WalletCreate(Wallet):
    user_id:str
class WalletInDB(Wallet):
    id:Optional[str]=None
    user_id:str

