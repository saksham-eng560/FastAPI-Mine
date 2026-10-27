import requests
from fastapi import FastAPI
import json
app = FastAPI()

@app.get("/")
def read_root():
    response = requests.get("https://jsonplaceholder.typicode.com/todos")
    return response.json()

