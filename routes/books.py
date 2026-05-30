from models.model import Book,Author
from sqlmodel import Session,select
from fastapi import HTTPException,Depends,status,APIRouter
from database.Session import get_session
from services.security import get_current_user
from schemas.book_schema import BookCreate,BookResponse,BookUpdate,BookSearch
from typing import List,Optional
import uuid
router=APIRouter(prefix="/books", tags=["Book"])
#creating the book router
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=BookResponse)
def create_book(book_data:BookCreate,session:Session=Depends(get_session),current_user:Book=Depends(get_current_user)):
    _book=Book(title=book_data.title,
    author_id=book_data.author_id,
    image_url=book_data.image_url,
    genre=book_data.genre,
    description=book_data.description,
    year=book_data.year)

    session.add(_book)
    session.commit()
    session.refresh(_book)

    return _book

#reading the book
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[BookResponse])
def get_book(session:Session=Depends(get_session),current_user:Book=Depends(get_current_user)):
    books=session.exec(select (Book)).all()
    return books

@router.get("/search",status_code=status.HTTP_200_OK,response_model=List[BookResponse])
def search_books(
    title: Optional[str] = None,author_name: Optional[str] = None,session: Session = Depends(get_session),current_user = Depends(get_current_user)):
    query = select(Book)

    if title is not None:
        query = query.where(Book.title.contains(title))

    if author_name is not None:
        authors = session.exec(select(Author).where(Author.name.contains(author_name))).all()
        author_ids = [author.id for author in authors]
        query = query.where(Book.author_id.in_(author_ids))

    books = session.exec(query).all()  
    return books                       

#reading book by id
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=BookResponse)
def get_book_by_id(id:uuid.UUID,session:Session=Depends(get_session),current_user:Book=Depends(get_current_user)):
    book=session.exec(select(Book).where(Book.id==id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found.")
    return book

#updating book by id
@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=BookResponse) 
def update_book_by_id(id:uuid.UUID,book_data:BookUpdate,session:Session=Depends(get_session),current_user:Book=Depends(get_current_user)):
    book=session.exec(select(Book).where(Book.id==id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found")
    
    if book_data.title is not None:
        book.title=book_data.title
       
    if book_data.author_id is not None:
        book.author_id = book_data.author_id
   
    if book_data.image_url is not None:
        book.image_url= book_data.image_url

    if book_data.genre is not None:
        book.genre= book_data.genre    
    
    if book_data.description is not None:
        book.description = book_data.description
    
    if book_data.year is not None:
        book.year= book_data.year

    session.add(book)  
    session.commit()  
    session.refresh(book)

    return book

#deleting the book
@router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_book_by_id(id:uuid.UUID,session:Session=Depends(get_session),current_user:Book=Depends(get_current_user)):
    book=session.exec(select(Book).where(Book.id == id)).first()

    if not book:
        raise HTTPException(status_code=404,detail="Book Not Found.")
    
    session.delete(book)
    session.commit()

    return{"message":"Book deleted Successfully!"}