from fastapi import Depends,HTTPException,status,APIRouter
from schemas.author_schema import AuthorCreate,BookInAuthor,AuthorResponse,AuthorUpdate
from sqlmodel import Session,select
from database.Session import get_session
from models.model import Author
from services.security import get_current_user
import uuid
router=APIRouter(prefix="/author",tags=["Author"])
#creating an author
@router.post("/",status_code=status.HTTP_201_CREATED ,response_model=AuthorResponse)
def create_author(author_data:AuthorCreate,session:Session=Depends(get_session),current_user:Author=Depends(get_current_user)):
    _author=Author(name=author_data.name)
    session.add(_author)
    session.commit()
    session.refresh(_author)

    return _author

#reading an author
@router.get("/",status_code=status.HTTP_200_OK,response_model=list[AuthorResponse])
def get_author(session:Session=Depends(get_session),current_user:Author=Depends(get_current_user)):
    authors=session.exec(select(Author)).all()
    return authors

#reading an author by id
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=AuthorResponse)
def get_author_by_id(id:uuid.UUID,session:Session=Depends(get_session),current_user:Author=Depends(get_current_user)):
    author= session.exec(select(Author).where(Author.id==id)).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not Found")
    return author

#updating an author's name by id
@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=AuthorResponse)
def update_author_by_id(id:uuid.UUID,author_data:AuthorUpdate, session:Session=Depends(get_session),current_user:Author=Depends(get_current_user)):
    author= session.exec(select(Author).where(Author.id==id)).first()
    if not author:
        raise HTTPException(status_code=404,detail="Author not Found")
    author.name=author_data.name
    session.add(author)
    session.commit()
    session.refresh(author)

    return author


@router.delete("/{id}",status_code=status.HTTP_200_OK)#we will not require an author response since will need a deletion success message
def delete_author_by_id(id:uuid.UUID,session:Session=Depends(get_session),current_user:Author=Depends(get_current_user)):
    author= session.exec(select(Author).where(Author.id==id)).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not Found.")
    session.delete(author)
    session.commit()
    
    
    return {"message":"Author deleted successfully!"}


