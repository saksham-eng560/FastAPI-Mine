# from fastapi import FastAPI, Depends
# from typing import Optional, Annotated

# app = FastAPI()

# #common logic or functino to be used
# async def common_logic(name : Optional[str] = None,age : Optional[int] = None,gender : Optional[str] = "not mention"):
#     return {
#         "name" : name,
#         "age" : age,
#         "gender" : gender
#     }
# # we can use annotated in small form also
# return_type = Annotated[dict,Depends(common_logic)]

# @app.get("/user/")
# async def user(id : return_type):
#     return id

# #Annotated means that the function will return dict so put it in a dict and this is the total type of id 
# #its annotated form of dict having value from depends(...)

# from typing import Annotated,Optional

# from fastapi import Cookie, Depends, FastAPI

# app = FastAPI()


# def query_extractor(q: Optional[str] = None):
#     return q


# def query_or_cookie_extractor(
#     q: Annotated[Optional[str], Depends(query_extractor)],
#     last_query: Annotated[Optional[str], Cookie()] = None):
#     if last_query is not None:
#         return last_query
#     return q


# @app.get("/items/")
# async def read_query(
#     query_or_default: Annotated[Optional[str], Depends(query_or_cookie_extractor)]):
#     return {"q_or_cookie": query_or_default}

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


# we can use the depends thing if we want a value we put it in
# the function and if we dont want the value just to make the function just run we can put them
# int the path decorator and multiple ones can be put in a list and in function we can create diff variable as values might be 
# reutrned
