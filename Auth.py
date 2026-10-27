from fastapi import FastAPI, HTTPException, Header,Depends
from jose import jwt
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
load_dotenv()
#jose - Javascript opject and script encryption

app = FastAPI()

# FLow of authentication
# user name and passd -> generate token -> verify toke -> accesss
#                                                      -> no access

#Token genreration
SECRET_KEY = os.getenv("SECRET_KEY") #we dont want to hardcode the secret key or show it in the code so we use the env file
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

#this creates the token and returns it to the usable function

#token decoder and verifier
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#normal api to check

@app.post("/login")
def login(username: str, password: str):
    # In a real application, you would verify the username and password against a database
    if username == "user" and password == "password":
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/check")
def check_token(token: str = Header(None)):
    payload = verify_token(token)
    return {"user": payload}