from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

class todo(BaseModel):
    task:str
    id:int
    completed:bool

app = FastAPI()

#CRUD

Todos: list[todo] = []

# CREATE

@app.post("/todo/")
async def create_task(task:todo):
    Todos.append(task)
    return {
        "mssg" : "task created!",
        "task" : task
    }

#READ

@app.get("/todo/tasks")
async def show_list():
    return Todos

#DELETE

@app.delete("/todo/{task_id}")
async def delete(task_id:int):
    for el in Todos:
        if el.id == task_id:
            Todos.remove(el)
            return{"message" : "task deleted"}
    raise HTTPException(status_code=404,detail="not found!")

#UPDATE

@app.put("/todo/update/{task_id}")
async def update(upd:todo,task_id:int):
    for el in Todos:
        if el.id == task_id:
            if el.task != upd.task:
                el.task = upd.task
            if el.completed != upd.completed:
                el.completed = upd.completed
        return {"message" : "updated!"}
    
    raise HTTPException(status_code=404,detail="not found!")
            
#raise http expception not return

#Response Model is the way in which i wanna give the info to the user

class UserRes(BaseModel):
    task:str
    completed:bool

@app.get("/todo/",response_model=UserRes)
async def res():
    return Todos


