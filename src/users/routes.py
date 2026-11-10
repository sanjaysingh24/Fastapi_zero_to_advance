from fastapi import APIRouter,Depends,status,Request
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.users.dtos import UserSchema,UserResponse,LoginSchema
from src.users import controller

user_routes = APIRouter(prefix="/user",tags=['User'])

@user_routes.post("/register",response_model =UserResponse,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)

@user_routes.post("/login",status_code=status.HTTP_200_OK)
def login(body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

@user_routes.get("/is_authenticate",status_code = status.HTTP_200_OK,response_model=UserResponse)
def is_authenticate(request:Request,db:Session=Depends(get_db)):
    return controller.is_auth(request,db)
    