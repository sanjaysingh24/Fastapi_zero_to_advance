from src.tasks.dtos import taskSchema,taskupdate
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException


def create_task(data: taskSchema, db: Session):

    body_data = data.model_dump()
    new_task = TaskModel(
        title=body_data["title"],
        description=body_data["description"],
        is_completed=body_data["is_completed"],
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_task(db:Session):
    tasks = db.query(TaskModel).all()
    return tasks


def get_single_task(Task_id:int,db:Session):
    one_task = db.query(TaskModel).get(Task_id)
    if not one_task:
        raise HTTPException(404,detail="Task Not Found")

    return one_task


def update_task(task_id:int,task_data:taskupdate,db:Session):
    '''check task id is correct or not'''
    check_task = db.query(TaskModel).get(task_id)
    if not check_task:
        raise HTTPException(404,detail="Task not found")
    # update the task
    updated_data = task_data.model_dump()
    for key,value in updated_data.items():
        setattr(check_task,key,value)
    #save changes
    db.commit()
    
    db.refresh(check_task)
    
    return check_task

def delete_task(task_id:int,db:Session):
    find_task = db.query(TaskModel).get(task_id)
    if not find_task:
        raise HTTPException(404,detail="Task Id Not Found")
    
    db.delete(find_task)
    db.commit()
    
    
    return None