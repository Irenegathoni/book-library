from pydantic import BaseModel

class user_registration(BaseModel):
    username:str
    email:str
    password:str
    confirm_password:str

class user_login(BaseModel):
    email:str
    password:str    