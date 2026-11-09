from src.users.dtos import UserSchema
from sqlalchemy.orm import Session
def register(body:UserSchema,db:Session):
    return{"message":"User Register Successfully"}