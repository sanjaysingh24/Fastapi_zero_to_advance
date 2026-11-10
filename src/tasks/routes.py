from fastapi import APIRouter,Depends,status
from src.tasks.dtos import taskSchema,taskupdate,taskResponse
from src.tasks.controller import create_task,get_task,get_single_task,update_task,delete_task
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src.users.models import UserModel
from src.utils.helpers import is_auth
task_routes = APIRouter(prefix="/tasks",tags=["Tasks"])

@task_routes.post("/create",response_model=taskResponse,status_code=status.HTTP_201_CREATED)
def task_create(data:taskSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_auth)):
    return create_task(data,db,user)


@task_routes.get("/alltask",response_model=List[taskResponse], status_code=status.HTTP_200_OK)
def getAll_task(db:Session=Depends(get_db),user:UserModel=Depends(is_auth)):
    return get_task(db,user)

@task_routes.get("/getsingle/{task_id}", response_model=taskResponse,status_code=status.HTTP_200_OK)
def getsingle_task(task_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_auth)):
    return get_single_task(task_id,db)

@task_routes.patch("/updatetask/{task_id}",response_model=taskResponse,status_code=status.HTTP_201_CREATED)
def taskupdates(task_id:int,task_data:taskupdate,db:Session=Depends(get_db),user:UserModel=Depends(is_auth)):
    return update_task(task_id,task_data,db,user)


@task_routes.delete("/deletetask/{task_id}",response_model=None,status_code=status.HTTP_204_NO_CONTENT)

def taskdelete(task_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_auth)):
    return delete_task(task_id,db,user)