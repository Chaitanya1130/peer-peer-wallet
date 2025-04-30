from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    
class transactionStatus(str,Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Transaction(BaseModel):
    amount:float
    

class TransactionCreate(Transaction):
    sender_username:str
    sender_email:str
    sender_balance:float
    receiver_username:str
    receiver_email:str
    receiver_balance:float
    amount:float
class TransactioninDB(Transaction):
    # id:Optional[str]=None
    sender_username:str
    sender_email:str
    sender_balance:float
    receiver_username:str
    receiver_email:str
    receiver_balance:float
    amount:float
