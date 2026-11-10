from src.users.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Request,BackgroundTasks
from pwdlib import PasswordHash
from src.users.models import UserModel
from src.utils.settings import settings
from datetime import datetime,timedelta
from src.utils.mail import send_email
from jwt.exceptions import InvalidTokenError
import jwt

password_hash = PasswordHash.recommended()


def gethashpass(password):
    return password_hash.hash(password)
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


async def register(body: UserSchema, db: Session,bg_task:BackgroundTasks):

    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exists")
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(400, detail="Email already exists")
    hash_password = gethashpass(body.password)
    new_user = UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        hash_password=hash_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
   
    bg_task.add_task(send_email,[new_user.email])
    
    return new_user



def login_user(body:LoginSchema,db:Session):
    #check username is valid or not
    is_username = db.query(UserModel).filter(UserModel.username==body.username).first()
    if not is_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    
    #verify the password 
    is_password = verify_password(body.password,is_username.hash_password)
    if not is_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    exp_time=datetime.now() + timedelta(minutes=settings.EXP_TIME)
    
    token = jwt.encode({"_id":is_username.id,"exp":exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)
    
    return{"token":token}

def is_auth(request:Request,db:Session):
    try:
        token =request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token is Required")
        token = token.split(" ")[-1]
        
        data = jwt.decode(token, settings.SECRET_KEY,settings.ALGORITHM)
        user_id = data.get("_id")
    
        is_user = db.query(UserModel).filter(UserModel.id==user_id).first()
        if not is_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")
        return is_user
    except InvalidTokenError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")
    