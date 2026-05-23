from pydantic import BaseModel
from typing import Optional,List
import uuid
class BookCreate(BaseModel):
    title:str
    author_id:uuid.UUID
    image_url:Optional[str]= None
    genre:str
    description:str
    year:int

class BookResponse(BaseModel):
    id:uuid.UUID
    title:str
    author_id:uuid.UUID
    image_url:Optional[str]=None
    genre:str
    description:str
    year:int

    model_config={"from_attributes":True}
    
class BookUpdate(BaseModel):
    title:Optional[str]=None
    author_id:Optional[uuid.UUID]=None
    image_url:Optional[str]= None
    genre:Optional[str]=None
    description:Optional[str]=None
    year:Optional[int]=None
