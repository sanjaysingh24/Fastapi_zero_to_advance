from fastapi import Request,HTTPException,status,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from src.utils.settings import settings
from sqlalchemy.orm import Session
from src.utils.db import get_db
import jwt
from jwt.exceptions import InvalidTokenError
from src.users.models import UserModel
security = HTTPBearer()
def is_auth(credentials:HTTPAuthorizationCredentials = Depends(security),db:Session=Depends(get_db)):
    try:
        token =credentials.credentials
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token is Required")
    
        
        data = jwt.decode(token, settings.SECRET_KEY,settings.ALGORITHM)
        user_id = data.get("_id")
    
        is_user = db.query(UserModel).filter(UserModel.id==user_id).first()
        if not is_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")
        return is_user
    except InvalidTokenError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")
    