from fastapi import APIRouter, Depends, HTTPException,Query
from bson import ObjectId
from pydantic import BaseModel
# routes/user.py
from app.models.wallet import Wallet, WalletCreate, WalletInDB
from app.models.user import User, UserCreate, UserInDB
from app.database import user_collection, wallet_collection
from app.models.transaction import Transaction, TransactionCreate ,TransactioninDB
from app.database import transaction_collection
from app.database import getUserID, getuserByusername, getuserByemail, getBalanceByusername
from langchain_ollama import OllamaLLM
# from app.utils import hash_password
router = APIRouter()
def HashPassword(password:str):
    hashedPass=""
    for char in password:
        hashedchar=chr(ord(char)+1)
        hashedPass+=hashedchar
    return hashedPass

def decryptPassword(hashedPass:str):
    password=""
    for char in hashedPass:
        originalchar=chr(ord(char)-1)
        password+=originalchar
    return password

@router.post("/signup", response_model=UserInDB)
async def create_user(user: UserCreate):
    curruser=await getuserByusername(user.username)

    if curruser:
        raise HTTPException(status_code=400, detail="Username already exists")
    else:
        new_useradta={
            "username":user.username,
            "email":user.email,
            "hash_pass":HashPassword(user.password),
        }
        result=await user_collection.insert_one(new_useradta)
        new_userid=result.inserted_id
        newWalletdat={
            "user_id":str(new_userid),
            "balance":0.0
        }
        wallet_result=await wallet_collection.insert_one(newWalletdat)
        new_walletid=wallet_result.inserted_id
        await user_collection.update_one({"_id":new_userid},{"$set":{"wallet_id":str(new_walletid)}})
        return UserInDB(
            id=str(new_userid),
            username=user.username,
            email=user.email,
            hash_pass=HashPassword(user.password),
             # This will print the original password
        
        )
    

@router.post("/login",response_model=UserInDB)
async def loginforuser(user:UserCreate):
    loggingUser=await getuserByusername(user.username)
    
    if not loggingUser:
        raise HTTPException(status_code=400, detail="User does not exists")
    else:
        if loggingUser["hash_pass"]!=HashPassword(user.password):
                    raise HTTPException(status_code=400, detail="Wrong password")

        return UserInDB(
            id=str(loggingUser["_id"]),
            username=user.username,
            email=user.email,
            hash_pass=loggingUser["hash_pass"]
        )
@router.get("/getDetails")
async def retriveDetails(username: str = Query(..., description="Username of the user to retrieve")):
    Curruser = await getuserByusername(username)
    
    # Log the entire user document to see what fields it actually contains
    print(f"User document: {Curruser}")
    
    wallet_id = Curruser.get("wallet_id")
    if not wallet_id:
        # Add more detailed error information
        raise HTTPException(status_code=404, detail=f"Wallet ID not found for user {username}. Available fields: {list(Curruser.keys())}")
    if isinstance(wallet_id, str):
        wallet_id = ObjectId(wallet_id)
    wallet = await wallet_collection.find_one({"_id": wallet_id})
    if not wallet:
        raise HTTPException(status_code=404, detail=f"Wallet not found for wallet_id: {wallet_id}")
    
    balance = wallet.get("balance")
    return UserInDB(
        id=str(Curruser["_id"]),
        username=Curruser["username"],
        email=Curruser["email"],
        hash_pass=Curruser["hash_pass"],
        balance=balance
    )

llm=OllamaLLM(model="llama2", temperature=0.9)
@router.post("/giveMEasuitablepassword")
async def ollamaGivespass(username:str):
     prompt = f"Generate a random example string with {len(username)} characters, combining letters, numbers, and symbols. Only output the string, no explanation."
     try:
          response=llm.invoke(prompt)
          gen_pass=response.strip()
          return {"username":username,"generaatedpassword":gen_pass}
     except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error generating password: {e}")

class BudgetAdviceRequest(BaseModel):
    username: str
    time: int
    
@router.post("/budgetadvice")
async def budgetAdvice(request:BudgetAdviceRequest):
     user=request.username
     time=request.time
     transactions=await transaction_collection.find({"sender_username":user}).to_list(length=time)
     if not transactions:
          raise HTTPException(status_code=404, detail="No transactions found for this user")
     else:
          prompt = f"Based on the transactions for {user} in the last {time}, make a ordered list of the amount he has sent in the transaction. For example 1.1000/- 2.10000/-."
          try:
               response=llm.invoke(prompt)
               advice=response.strip()
               return {"username":user,"advice":advice,"time":time}
          except Exception as e:
               raise HTTPException(status_code=500, detail=f"Error generating budget advice: {e}")