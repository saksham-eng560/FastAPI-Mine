from fastapi import FastAPI, Query, Request
from typing import Optional
from models import UserStructure
from pydantic import BaseModel
from enum import Enum
from fastapi.responses import JSONResponse
#imports
class exceptions(Exception):
    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age

app = FastAPI()

@app.exception_handler(exceptions)
async def error_handler(res : Request,exc:exceptions):
    return JSONResponse(
        status_code=418,
        content={"message": f"u fucked up {exc.name} of age {exc.age} am sorry mate"}
    )

@app.get("/error/{name_id}/{age}")
async def error(name_id:str,age:int):
    if name_id == "saksham" and age == 17:
        raise exceptions(name_id,age)
    return {"message" : "welcome!"}

@app.get("/")
async def hello():
    return {"message" : "hello world"}

@app.get("/user/{user_id}")
async def users(user_id):
    return {
        "user_id" : user_id
    }

#we can define the type od dynamic paramteter which is passed
@app.get("/users/{user_id}")
async def users(user_id:str):#or int
    return {
        "user_id" : user_id
    }

@app.get("/items/{limit}")
def get_items(limit: int):
    # 'limit' defaults to 10 if omitted from the URL
    return {"limit": limit}

# users/{user_id} in this user id is a path parameter
#if i use users/?name=saksham&age=18 then name and age are query parameter these are used for filtering,
#searching,sorting,pagnation etcd

@app.get("/person/{user_id}")
async def per(user_id:int,name :Optional[str] = "saksham",age :int = Query(...)):
    return {
        "user_id":user_id,
        "name":name,
        "age":age
    }

#int this a path parameter user_id i required and if not provided then wont work as no default value is set
#path parameters have no default value.
#for it like the name and age
#naem and age are the query parameters automatically as they are not written in the path and if not provided have 
#default values

from typing import Optional

@app.get("/items/")
def get_items(q:Optional[str] = "hello"):
    if q != "hello":
        return {"search": q}
    return {"search": "blah!"}

#why do we use pydantic models for eg if without that

@app.post("/create/")
async def create_user(name : Optional[str] = "default",gen : str = Query(...)): #in the function parameter i will have to write what will i get
    return{
        "name" : name,
        "gender" : gen
    }
#but pydantic makes it way easier adn shortens it out so i dont have to write all parmaeter
#plus handles the data verification part

#Query(...) this means its required

@app.post("/createdict/")
async def creater(User : UserStructure): #in the function parameter i will have to write what will i get
    return{
        "data" : User
    }

#parameters (int,str,dict,list,etc)

#pydantic creates a default schema which depicts the base structure of the post request

class Models(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_id}")
async def model(model_id : Models):
    if model_id == Models.alexnet.value:
        return {"model" : model_id}
    if model_id == Models.resnet:
        return {"model" : model_id}
    if model_id == "lenet":
        return {"model" : model_id}
    return {"specify the model please"}

#the path parameter can be a int , str , enum and a path itself!

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

#In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home.

#annotations