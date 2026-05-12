import bcrypt
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from config import settings
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import APIRouter,Depends,HTTPException,status
from database.Session import get_session
from sqlmodel import Session
#configuring the hashing algorithm
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#hashing the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#verifying the hashed password and plain password
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
 

#creating access tokens
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm="HS256")

#creating a current user function
security_scheme=HTTPBearer()
ALGORITHM="HS256"
def get_current_user(credentials:HTTPAuthorizationCredentials =Depends(security_scheme),session :Session= Depends(get_session)):
    token =credentials.credentials
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        