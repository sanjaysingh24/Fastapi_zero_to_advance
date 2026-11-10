from pydantic import BaseModel

class taskSchema(BaseModel):
    title:str
    description:str
    is_completed:bool = False
    
    
class taskupdate(BaseModel):
    title:str | None = None
    description:str | None = None
    is_completed:bool | None  = None
    
    
class taskResponse(BaseModel):
    id:int
    title:str
    description:str
    is_completed:bool
    userId:int | None=None