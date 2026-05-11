#import typing library
from typing import List,Optional
#import the sqlmodel library
from sqlmodel import SQLModel, Field,Relationship
import uuid
import psycopg2
#define the user table
class User(SQLModel,table=True):
  #1. id(primary key)
  id:Optional[uuid.UUID]=Field(default_factory=uuid.uuid4,primary_key=True)
  #2.username
  username:str=Field(unique=True,index=True)
  #3.email
  email:str=Field(unique=True)
  #4.hashed_password - has to be hashed and not plain
  hashed_password:str

  #define the relationship between the user and userbook(one userhas many userbooks)
  user_book:List["UserBook"]=Relationship(back_populates="user")

#define the author table
class Author(SQLModel,table=True):
   id:Optional[uuid.UUID]=Field(default_factory=uuid.uuid4,primary_key=True)
   name:str

   #define the relationship between the author and the book
   book:List["Book"]=Relationship(back_populates="author")


#define the book table
class Book(SQLModel,table=True):
   #1.id(primary key)
   id:Optional[uuid.UUID]=Field(default_factory=uuid.uuid4,primary_key=True)
   #2.author_id
   author_id:Optional[uuid.UUID]=Field(foreign_key="author.id")
   # 3.title
   title:str
   #4.image url 
   image_url:Optional[str]=None 
   #5.genre
   genre:str 
   #6.description
   description:str
   #7.year
   year:int


   #define the relationship between the book and the author 
   author:Optional["Author"]=Relationship(back_populates="book")
   #define the relationship between the book and the userbook
   user_book:List["UserBook"]=Relationship(back_populates="book")


#define the userbook table
class UserBook(SQLModel,table=True):
   id:Optional[uuid.UUID]=Field(default_factory=uuid.uuid4,primary_key=True)
   user_id:Optional[uuid.UUID]=Field(foreign_key="user.id")
   book_id:Optional[uuid.UUID]=Field(foreign_key="book.id")
   status:str

   #relationship between the user and the userbook(one user can read one book)
   user:Optional[User]=Relationship(back_populates="user_book")


   #relationship between the book and userbook(one entry point to one  book)
   book:Optional[Book]=Relationship(back_populates="user_book")