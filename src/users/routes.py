from fastapi import APIRouter,Depends,status
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.users.dtos import UserSchema,UserResponse
from src.users import controller
user_routes = APIRouter(prefix="/user",tags=['User'])

@user_routes.post("/register",response_model =UserResponse,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)

    