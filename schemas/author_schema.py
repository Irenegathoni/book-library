from pydantic import BaseModel
import uuid
from typing import Optional,List
class AuthorCreate(BaseModel):
    name:str

class BookInAuthor(BaseModel):
    id:uuid.UUID
    title:str
    genre:str
    description:str
    year:int
    image_url:Optional[str]=None

    model_config={"from_attributes":True}

class AuthorResponse(BaseModel):
    id:uuid.UUID
    name:str
    books:List[BookInAuthor] =[]   
     
    #this tells pydantic to read data from SQLModel objects instead of expecting a plain dictionary
    model_config= {"from_attributes":True}