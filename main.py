from fastapi import FastAPI 
from src.utils.db import Base,engine
from src.tasks.routes import task_routes
from src.users.routes import user_routes
Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(task_routes)
app.include_router(user_routes)
@app.get("/health",tags=['server'])
def root():
    return{"message":"Welcome to the server"}