from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session,select
from database.Session import get_session # from the session generator
from models.model import User # from the User Model
from services.security import hash_password,verify_password,create_access_token,get_current_user
from schemas.user_schema import user_registration,user_login
from jose import JWTError, jwt
from config import settings
router=APIRouter(prefix="/auth",tags=["Auth"])
@router.post ("/register",status_code=status.HTTP_201_CREATED)
#CHECKING FOR EXISTING USER
def register(user_data:user_registration,session:Session=Depends(get_session)):
    existing_user=session.exec(select(User).where(User.email==user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists")
    
#checking for password
    if user_data.password !=user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Password doesn't match")
    
#hashed password
    hashed=hash_password(user_data.password)
    
    
        

#creating new user     
    new_user=User(username=user_data.username,email=user_data.email,hashed_password=hashed)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return{"message":"Registration Successful","username":new_user.username}
  
#USER LOGIN

@router.post("/login",status_code=status.HTTP_200_OK)
def login(login_data:user_login,session:Session=Depends(get_session)):
    user=session.exec(select(User).where(User.email==login_data.email)).first()

    if user is None:
        raise HTTPException(status_code=400, details="Incorrect Email")
    if not verify_password(login_data.password,user.hashed_password):
        raise HTTPException(status_code=400,detail="Incorrect Password")
    
        
    token=create_access_token(data={"sub":str(user.id)})

    return{"access token":token,"token_type":"bearer"}


#creating a "ME" function
@router.get("/me")
def get_me(current_user:str=Depends(get_current_user),session:Session=Depends(get_session)):
    return current_user