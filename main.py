from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.authors import router as author_router
from routes.books import router as book_router
app=FastAPI(title="Book Library")

app.include_router(auth_router)
app.include_router(author_router)
app.include_router(book_router)
@app.get("/")

def home():
    return{"message":"Welcome to the Book Library"}
