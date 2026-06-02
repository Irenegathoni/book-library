from pydantic import BaseModel
from enum import Enum
import uuid
from typing import List,Optional

class ReadingStatus(str,Enum):
    reading="reading"
    finished="finished"
    want_to_read="want_to_read"

class UserBookCreate(BaseModel):
    book_id:uuid.UUID
    status:ReadingStatus
   
class UserBookResponse(BaseModel):
    id:uuid.UUID
    book_title:str
    book_genre:str
    author_name:str
    status:ReadingStatus
    model_config={"from_attributes":True}

class UserBookUpdate(BaseModel):
    book_title:Optional[str]=None
    book_genre:Optional[str]=None
    author_name:Optional[str]=None
    status:List[ReadingStatus]=[]
