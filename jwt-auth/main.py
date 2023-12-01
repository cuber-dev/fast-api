import cv2 
import base64

from fastapi import FastAPI, Path,Body, Depends, File ,HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends

from app.schema import PostSchema , UserSchema , UserLoginSchema
from app.auth.jwt_handler import signJWT,decodeJWT
from app.auth.jwt_bearer import jwt_bearer
from starlette.responses import FileResponse

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware settings
origins = ["http://localhost", "https://localhost"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# the users database , for now an array but in production we need SQL or mongo_db
users = [
    {
        "email" : "marcus9@gmail.com",
        "password" : "123"
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


@app.post("/grayscale/{image_name}", dependencies=[Depends(jwt_bearer())])
def grayscale(image_name: str, image: UploadFile = File(...)):
    # storing the original image
    with open('./img_db/original/' + image_name, 'wb') as f:
        f.write(image.file.read())

    # processeing original image
    ori_image = cv2.imread('./img_db/original/' + image_name)
    gray_img = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)

    # storing the processed image
    cv2.imwrite(f'./img_db/processed/grayscale_{image_name}', gray_img)

    # converting image to base64 string for avoiding cors erros in frontend
    gray_base64 = img_res_base64(gray_img)
    return {
        "grayscale_img": gray_base64
    }



# we can enable this route to register their accounts 
# @app.post("/users/sign-up")
# async def sign_up(user: UserSchema = Body(default=None)):
#     users.append(user.dict())
#     return signJWT(user.email)


# this route is for validating the user credintials.
@app.post("/login")
async def login(user: UserLoginSchema = Body(default=None)):
    if validate_user(user):
        return signJWT(user.email)
    return HTTPException(status_code=401, detail="Invalid Credentials")
def validate_user(data : UserLoginSchema):
    for user in users:
        if user["email"] == data.email and user["password"] == data.password:
            print("user has a account : ",user)
            return True
    return False

# this route is for validating the JWT Token.
@app.get("/validate-t/{jwt}")
def login(jwt : str):
    print("===================================================================")
    print("original jwt : ",jwt)
    decoded_jwt = decodeJWT(jwt)
    print("decoded jwt : ",decoded_jwt)
    if len(decoded_jwt) != 0:
        for user in users:
            if user["email"] == decoded_jwt["email"]:
                print("user jwt token is valid : ",user)
                print("===================================================================")

                return { "is_valid_jwt" : True}
    print("user jwt token is invalid and his credintials are : ",decoded_jwt)
    print("===================================================================")

    return HTTPException(status_code=401, detail="Invalid token, please login again!")
 

@app.get("/")
def read_root():
    return { "msg" : "server is running!"}
# ===========================================================================================
# ===========================================================================================
# ===========================================================================================
