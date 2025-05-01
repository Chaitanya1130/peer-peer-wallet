from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from bson import ObjectId
# routes/user.py
# from models.wallet import Wallet, WalletCreate, WalletInDB
from app.models.user import User, UserCreate, UserInDB
from app.database import user_collection, wallet_collection
from app.database import getUserID, getuserByusername, getuserByemail, getBalanceByusername
from app.models.transaction import Transaction, TransactionCreate ,TransactioninDB
from app.database import transaction_collection




router=APIRouter()
# @router.put("/credit")
# async def creditMoney(username:str,amount:float):
#     if amount<=0:
#         raise HTTPException(status_code=404, detail="money cannot be less than/equal to zero")
#     user=await getuserByusername(username)
#     if not user:
#         raise HTTPException(status_code=404, detail="User does not exist")
#     wallet=await wallet_collection.find_one({"_id":user["wallet_id"]})
#     if not wallet:
#         raise HTTPException(status_code=404, detail="Wallet does not exist")
#     new_balance=wallet["balance"]+amount
#     await wallet_collection.update_one({"_id":user["wallet_id"]},{"$set":{"balance":new_balance}})
#     return UserInDB(
#         id=str(user["_id"]),
#         username=user["username"],
#         email=user["email"],
#         balance=new_balance,
#         hash_pass=user["hash_pass"]
#     )
class CreditRequest(BaseModel):
    username: str
    amount: float

@router.put("/credit")
async def creditMoney(request: CreditRequest = Body(...)):
    username = request.username
    amount = request.amount
    
    print(f"Processing credit request for {username} with amount {amount}")
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="money cannot be less than/equal to zero")
    
    user = await getuserByusername(username)
    print(f"User found: {user is not None}")
    
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    # Ensure wallet_id exists
    wallet_id = user.get("wallet_id")
    if not wallet_id:
        raise HTTPException(status_code=404, detail="User has no associated wallet_id")
    wallet_object_id = ObjectId(wallet_id)
    print(f"Looking for wallet with ID: {wallet_id}")
    wallet = await wallet_collection.find_one({"_id": wallet_object_id})
    print(f"Wallet found: {wallet is not None}")
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet does not exist")
    
    new_balance = wallet["balance"] + amount
    await wallet_collection.update_one({"_id": wallet_object_id}, {"$set": {"balance": new_balance}})
    
    return UserInDB(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        hash_pass=user["hash_pass"],
        balance=new_balance
    )


class CreditBetweenTwopeople(BaseModel):
    senderUsername:str
    receiverUsername:str
    amount:float

# @router.put("/creditMoney")
# async def creditThemMoney(request:CreditBetweenTwopeople=Body(...)):
#     sendingperson_username=request.senderUsername
#     receivingperson_username=request.receiverUsername
#     amount=request.amount
#     if amount<=0:
#         raise HTTPException(status_code=(404),detail="amount less than or equal to zero")
#     sender=await getuserByusername(sendingperson_username)
#     receiver=await getuserByusername(receivingperson_username)
#     if not sender or not receiver :
#         raise HTTPException(status_code=(400),detail="sender or reveiver not available")
#     else:
#         sender_wallet= sender.get("wallet_id")
#         receiver_wallet= receiver.get("wallet_id")
#         if not sender_wallet or not receiver_wallet:
#             raise HTTPException(status_code=404, detail="User has no associated wallet_id")
#         sendingWalletobjid=ObjectId(sender_wallet)
#         receivingWalletobjid=ObjectId(receiver_wallet)
#         senderWallet=await wallet_collection.find_one({"_id":sendingWalletobjid})
#         receiverWallet=await wallet_collection.find_one({"_id":receivingWalletobjid})
#         if not sender_wallet or receiverWallet:
#             raise HTTPException(status_code=(404),detail="wallet not found")
#         if senderWallet["balance"]<amount:
#             raise HTTPException(status_code=(400),detail="insufficent funds")
    
#         new_balanceForsender=senderWallet["balance"]-amount
#         new_balanceForreceiver=receiverWallet["balance"]+amount
#         await wallet_collection.update_one({"_id":sendingWalletobjid},{"$set":{"balance":new_balanceForsender}})
#         await wallet_collection.update_one({"_id":receivingWalletobjid},{"$set":{"balance":new_balanceForreceiver}})
#         transaction = TransactionCreate(
#         senderUsername=sender["username"],
#         senderemail=sender["email"],
#         senderBalance=new_balanceForsender,
#         receiverUsername=receiver["username"],
#         receiveremail=receiver["email"],
#         receiverBalance=new_balanceForreceiver,
#         amount=amount
#     )
#         transaction_doc = transaction.dict()
#         await transaction_collection.insert_one(transaction_doc)
#         return TransactioninDB(
#             # id=str(sender["_id"]),
#             senderUsername=sender["username"],
#             senderemail=sender["email"],
#             senderBalance=senderWallet["balance"],
#             receiverUsername=receiver["username"],
#             receiveremail=receiver["email"],
#             receiverBalance=receiverWallet["balance"],
#         )
@router.put("/creditMoney")
async def creditThemMoney(request:CreditBetweenTwopeople=Body(...)):
    sendingperson_username=request.senderUsername
    receivingperson_username=request.receiverUsername
    amount=request.amount
    if amount<=0:
        raise HTTPException(status_code=400, detail="amount less than or equal to zero")
    
    # Get user documents
    sender=await getuserByusername(sendingperson_username)
    receiver=await getuserByusername(receivingperson_username)
    
    if not sender or not receiver:
        raise HTTPException(status_code=400, detail="sender or receiver not available")
    
    # Get wallet IDs
    sender_wallet_id = sender.get("wallet_id")
    receiver_wallet_id = receiver.get("wallet_id")
    
    if not sender_wallet_id or not receiver_wallet_id:
        raise HTTPException(status_code=404, detail="User has no associated wallet_id")
    
    # Convert to ObjectId
    sendingWalletobjid = ObjectId(sender_wallet_id)
    receivingWalletobjid = ObjectId(receiver_wallet_id)
    
    # Get wallet documents
    senderWallet = await wallet_collection.find_one({"_id": sendingWalletobjid})
    receiverWallet = await wallet_collection.find_one({"_id": receivingWalletobjid})
    
    # Check if wallets exist
    if not senderWallet or not receiverWallet:
        raise HTTPException(status_code=404, detail="wallet not found")
    
    # Check if sender has enough balance
    if senderWallet["balance"] < amount:
        raise HTTPException(status_code=400, detail="insufficient balance")
    
    # Update balances
    new_balanceForsender = senderWallet["balance"] - amount
    new_balanceForreceiver = receiverWallet["balance"] + amount
    
    await wallet_collection.update_one({"_id": sendingWalletobjid}, {"$set": {"balance": new_balanceForsender}})
    await wallet_collection.update_one({"_id": receivingWalletobjid}, {"$set": {"balance": new_balanceForreceiver}})
    
    # Create transaction record
    transaction = TransactionCreate(
        sender_username=sender["username"],
        sender_email=sender["email"],
        sender_balance=new_balanceForsender,
        receiver_username=receiver["username"],
        receiver_email=receiver["email"],
        receiver_balance=new_balanceForreceiver,
        amount=amount
    )
    
    transaction_doc = transaction.dict()
    await transaction_collection.insert_one(transaction_doc)
    
    return TransactioninDB(
        sender_username=sender["username"],
        sender_email=sender["email"],
        sender_balance=new_balanceForsender,
        receiver_username=receiver["username"],
        receiver_email=receiver["email"],
        receiver_balance=new_balanceForreceiver,
        amount=amount
    )

class GetTransaction(BaseModel):
    username:str

@router.get("/getRecentTransactions")
async def getTransaction(username:str=Query(..., description="Username of the user to retrieve")):
    user=await getuserByusername(username)
    # user=await getuserByusername(username)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    else:
        transactions = await transaction_collection.find({"$or": [{"sender_username": username}, {"receiver_username": username}]}).to_list(length=1)
        return TransactioninDB(
            sender_username=transactions[0]["sender_username"],
            sender_email=transactions[0]["sender_email"],
            sender_balance=transactions[0]["sender_balance"],
            receiver_username=transactions[0]["receiver_username"],
            receiver_email=transactions[0]["receiver_email"],
            receiver_balance=transactions[0]["receiver_balance"],
            amount=transactions[0]["amount"]
        )