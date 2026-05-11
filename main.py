from fastapi import FastAPI
from routes.auth import router as auth_router

app=FastAPI(title="Book Library")

app.include_router(auth_router)
@app.get("/")

def home():
    return{"message":"Welcome to the Book Library"}
