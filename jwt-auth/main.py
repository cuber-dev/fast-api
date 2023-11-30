import os
import cv2 
import numpy as np
import base64

from fastapi import FastAPI, Body, Depends, File ,HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from app.schema import PostSchema , UserSchema , UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwt_bearer
from starlette.responses import FileResponse

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware settings
origins = ["http://localhost", "https://localhost"]  # Add your frontend origins here

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
users = [
    {
        "email" : "marcus9@gmail.com",
        "password" : "123"
    }
]

posts = [
    {
        "id": 1,
        "title": "First post",
        "content": "This is the first post"
    },
    {
        "id": 2,
        "title": "Second post",
        "content": "This is the second post"
    },
    {
        "id": 3,
        "title": "Third post",
        "content": "This is the third post"
    }
]



# ===========================================================================================
# ============= JWT-AUTH - login testing with a sample software =============================
# ===========================================================================================
# this is for converting image to base64 string for avoiding cors erros in frontend
def img_res_base64(img):
    # first base64 format string and second base64 string
    return "data:image/jpeg;base64," + base64.b64encode(
        cv2.imencode(".jpg", img)[1].tobytes()
    ).decode()

@app.post("/grayscale",dependencies=[Depends(jwt_bearer())])
def grayscale(image: UploadFile = File(...)):
    with open('./img_db/original/or_img.jpg', 'wb') as f:
        f.write(image.file.read())
  
    temp_img = cv2.imread('./img_db/original/or_img.jpg')
    img = temp_img
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    gray_base64 = img_res_base64(gray_img)
  
    return {
        "grayscale_img": gray_base64
    }
# ===========================================================================================
# ===========================================================================================
# ===========================================================================================

@app.get("/posts/get/{id}")
async def get_post(id: int):
    for post in posts:
        if post["id"] == id:
            return {
                "post": post
            }
    return {
        "Error" : "can\'t find posts with id : " + str(id)
    }



@app.post("/posts/create", dependencies=[Depends(jwt_bearer())])
async def create_post(post: PostSchema):
    for item in posts:
        if item["id"] == post.id:
            return {
                "Error": "Post already exists with id : " + str(post.id)
            }
    posts.append(post.dict())
    return {
        "success" : "Post added succesfully",
        "post": post
    }


@app.post("/users/sign-up")
async def sign_up(user: UserSchema = Body(default=None)):
    users.append(user.dict())
    return signJWT(user.email)


@app.post("/users/login")
async def login(user: UserLoginSchema = Body(default=None)):
    if validate_user(user):
        return signJWT(user.email)
    return HTTPException(status_code=401, detail="Invalid Credentials")

def validate_user(data : UserLoginSchema):
    for user in users:
        if user["email"] == data.email and user["password"] == data.password:
            print(user)
            return True
    return False

@app.get("/")
def read_root():
    return { "msg" : "server is running!"}
#     index_path = os.path.join("./public", "index.html")
#     return FileResponse(index_path)
# app.mount("/", StaticFiles(directory="./public"), name="static")
