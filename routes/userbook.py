from models.model import UserBook,Book,Author,User
from fastapi import APIRouter,HTTPException,Depends,status
from sqlmodel import Session,select
from services.security import get_current_user
from database.Session import get_session
from schemas.userbook_schema import UserBookCreate,UserBookResponse,UserBookUpdate
from typing import List,Optional
import uuid
router=APIRouter(prefix="/userbook",tags=["UserBooks"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserBookResponse)
def create_userbook(userbook_data:UserBookCreate,session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
   #cheking if the book already exists
   book=session.exec(select(Book).where(Book.id==userbook_data.book_id)).first()
   if book is None:
    raise HTTPException(status_code=404,detail="Book not found.")
   
   #checking if the user has already  added the book
   existing_book=session.exec(select(UserBook).where(UserBook.user_id==current_user.id,UserBook.book_id==userbook_data.book_id)).first()
   if existing_book:
    raise HTTPException(status_code=400,detail="Book already exists in the list")
   
   #getting the author's name
   author=session.exec(select(Author).where(Author.id==book.author_id)).first()


   _userbook=UserBook(user_id=current_user.id,
            book_id=userbook_data.book_id,         
            status=userbook_data.status)

   session.add(_userbook)
   session.commit()
   session.refresh(_userbook)

   return UserBookResponse(
        id=_userbook.id,
        status=_userbook.status,
        book_title=book.title,
        book_genre=book.genre,
        author_name=author.name if author else "Unknown"
    )

@router.get("/",status_code=status.HTTP_202_ACCEPTED,response_model=List[UserBookResponse])
def get_userbooks(session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
    userbooks=session.exec(select(UserBook).where(UserBook.user_id==current_user.id)).all()
    response=[]
    for userbook in userbooks:
        book=session.exec(select(Book).where(Book.id==userbook.book_id)).first()
        author=session.exec(select(Author).where(Author.id==book.author_id)).first() if book else None
        response.append(UserBookResponse(
            id=userbook.id,
            status=userbook.status,
            book_title=book.title if book else "Unknown",
            book_genre=book.genre if book else "Unknown",
            book_description=book.description if book else "Unknown",
            book_year=book.year if book else 0,
            author_name=author.name if author else "Unknown"
        ))
    return response

@router.patch("/{id}",status_code=status.HTTP_200_OK,response_model=UserBookResponse)
def update_userbook(id:uuid.UUID,userbook_data:UserBookUpdate,session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
    userbook=session.exec(select(UserBook).where(UserBook.id==id,UserBook.user_id==current_user.id)).first()
    if not userbook:
        raise HTTPException(status_code=404,detail="UserBook not found.")
    
    book=session.exec(select(Book).where(Book.id==userbook.book_id)).first()
    author=session.exec(select(Author).where(Author.id==book.author_id)).first() if book else None

    if userbook_data.status is not None:
        userbook.status=userbook_data.status
    
    session.add(userbook)
    session.commit()
    session.refresh(userbook)

    return UserBookResponse(
        id=userbook.id,
        status=userbook.status,
        book_title=book.title if book else "Unknown",
        book_genre=book.genre if book else "Unknown",
        author_name=author.name if author else "Unknown"
    )
   
#reading my book list
@router.get("/mybooks",status_code=status.HTTP_200_OK,response_model=List[UserBookResponse])
def get_mybooks(session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
    userbooks=session.exec(select(UserBook).where(UserBook.user_id==current_user.id)).all()
    response=[]
    for userbook in userbooks:
        book=session.exec(select(Book).where(Book.id==userbook.book_id)).first()
        author=session.exec(select(Author).where(Author.id==book.author_id)).first() if book else None
        response.append(UserBookResponse(
            id=userbook.id,
            status=userbook.status,
            book_title=book.title if book else "Unknown",
            book_genre=book.genre if book else "Unknown",
            book_description=book.description if book else "Unknown",
            book_year=book.year if book else 0,
            author_name=author.name if author else "Unknown"
        ))
    return response