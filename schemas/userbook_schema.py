from pydantic import BaseModel
from enum import Enum
import uuid
from typing import List

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