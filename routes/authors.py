from fastapi import Depends,HTTPException,status,APIRouter
from schemas.author_schema import AuthorCreate,BookInAuthor,AuthorResponse
from sqlmodel import Session,select
from database.Session import get_session
from models.model import Author
from services.security import get_current_user

router=APIRouter(prefix="/author",tags=["Author"])
@router.post("/",status_code=status.HTTP_201_CREATED ,response_model=AuthorResponse)
def create_author(author_data:AuthorCreate,session:Session=Depends(get_session),current_user:Author=Depends(get_current_user)):
    _author=Author(name=author_data.name)
    session.add(_author)
    session.commit()
    session.refresh(_author)

    return _author

