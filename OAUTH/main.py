
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Simulated database
fake_users_db = {}
fake_blogs_db = []

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class Blog(BaseModel):
    title: str
    content: str

class BlogInDB(Blog):
    author: str

# OAuth2PasswordBearer for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify user credentials
def verify_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and pwd_context.verify(password, user.hashed_password):
        return user

# Function to generate access token
def generate_access_token(data: dict):
    access_token_expires = timedelta(hours=2)
    access_token_data = {
        "sub": data["username"],
        "password": data["password"],
        "exp": datetime.utcnow() + access_token_expires
    }
    access_token = jwt.encode(access_token_data, "1891has1981", algorithm="HS256")
    return access_token

# Function to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "1891has1981", algorithms=["HS256"])
        print(payload)
        user = verify_user(payload["sub"], payload["password"])
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/signup")
def sign_up(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    fake_users_db[user.username] = UserInDB(**user.dict(), hashed_password=hashed_password)
    return {"message": "User registered successfully"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = generate_access_token({"username": user.username , "password": user.password})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/post", response_model=Blog)
def create_post(blog: Blog, current_user: User = Depends(get_current_user)):
    new_post = BlogInDB(**blog.dict(), author=current_user.username)
    fake_blogs_db.append(new_post)
    return new_post

@app.get("/posts", response_model=List[Blog])
def get_posts():
    return fake_blogs_db
