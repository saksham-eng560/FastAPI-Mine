from fastapi import FastAPI, HTTPException, Depends
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated

app = FastAPI()

# passlib 1.7.4 cannot initialize with bcrypt 5.x, which prevented this
# module from importing and therefore prevented Uvicorn from starting.
# PBKDF2-SHA256 is fully supported by passlib and needs no native bcrypt backend.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = "secret_key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

already_present_users = {
    "saksham": {"hashed_password": hash_password("valorant560")},
    "sachin": {"hashed_password": hash_password("sachin123")},
    "vedanshi": {"hashed_password": hash_password("veda")},
}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in already_present_users:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {
            "sub": username,
            "message": "Token is valid",
            "exp": payload["exp"],
        }
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
 

@app.post("/login")
async def login_interface(form_data: OAuth2PasswordRequestForm = Depends()):
    user = already_present_users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

 #formdata is nothing it just capture the username and passowrd in a class creates the object of that class and pass it to the function as a parameter. It is a dependency injection. we can use the formdata object to get the username and password from the request.

@app.get("/use",dependencies=[Depends(verify_access_token)])
async def access():
    return {
        "message" : "hello !"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("oAuth:app", host="127.0.0.1", port=8000, reload=True)
