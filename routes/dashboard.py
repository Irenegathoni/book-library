from schemas.dashboard_schema import DashboardResponse
from fastapi import APIRouter,Depends,status,HTTPException
from sqlmodel import Session,select
from services.security import get_current_user
from database.Session import get_session
from models.model import UserBook,Book,User,Author   
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])

@router.get("/",status_code=status.HTTP_200_OK,response_model=DashboardResponse)
def get_dashboard(session:Session=Depends(get_session),current_user=Depends(get_current_user)):
    #1. count the number of books read by the user
    books_read = session.exec(select(UserBook).where(UserBook.user_id == current_user.id,UserBook.status == "finished")).all()
    books_read_count = len(books_read)
    #2. get the currently reading book
    currently_reading_book=session.exec(select(UserBook).where(UserBook.user_id==current_user.id,UserBook.status=="reading")).first()
    
    if currently_reading_book:
        book=session.exec(select(Book).where(Book.id==currently_reading_book.book_id)).first()
        if book:
            return DashboardResponse(
                books_read_count=books_read_count,
                currently_reading=book.title,
                current_book_genre=book.genre,
                current_book_image=book.image_url
            )
    
    return DashboardResponse(books_read_count=books_read_count)
