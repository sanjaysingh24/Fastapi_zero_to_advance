from pydantic import BaseModel


class UserSchema(BaseModel):
    name:str
    password:str
    email:str
    username:str
    
class UserResponse(BaseModel):
    username:str
    email:str