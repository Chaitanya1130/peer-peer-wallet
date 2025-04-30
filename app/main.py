from fastapi import FastAPI
from app.routes import user, transaction
app= FastAPI()

# app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(transaction.router, prefix="/transaction", tags=["transaction"])
# app.include_router(transaction.router)