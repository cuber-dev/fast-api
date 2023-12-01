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
# ============= JWT-AUTH - login testing with a sample software. =============================
# ===========================================================================================

# Function to convert image to base64 string.
def img_res_base64(img):
    return "data:image/jpeg;base64," + base64.b64encode(
        cv2.imencode(".jpg", img)[1].tobytes()
    ).decode()

# Route for processing and returning a grayscale image.
@app.post("/grayscale/{image_name}", dependencies=[Depends(jwt_bearer())])
def grayscale(image_name: str, image: UploadFile = File(...)):
    # Storing the original image
    with open('./img_db/original/' + image_name, 'wb') as f:
        f.write(image.file.read())

    # Processing the original image to grayscale.
    ori_image = cv2.imread('./img_db/original/' + image_name)
    gray_img = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)

    # Storing the processed image
    cv2.imwrite(f'./img_db/processed/grayscale_{image_name}', gray_img)

    # Converting image to base64 string for avoiding CORS errors in frontend.
    gray_base64 = img_res_base64(gray_img)
    return {
        "grayscale_img": gray_base64
    }

# Route for user login.
@app.post("/login")
async def login(user: UserLoginSchema = Body(default=None)):
    if validate_user(user):
        return signJWT(user.email)  # This will generate a JWT token and return it to the user.
    return HTTPException(status_code=401, detail="Invalid Credentials")

# Function to validate user credentials.
def validate_user(data: UserLoginSchema):
    for user in users:
        if user["email"] == data.email and user["password"] == data.password:
            print("User has an account: ", user)
            return True
    return False

# Route for validating the JWT Token.
@app.get("/validate-t/{jwt}")
def validate_token(jwt: str):
    print("===================================================================")
    print("Original JWT: ", jwt)
    decoded_jwt = decodeJWT(jwt)
    print("Decoded JWT: ", decoded_jwt)
    if len(decoded_jwt) != 0:
        for user in users:
            if user["email"] == decoded_jwt["email"]:
                print("User JWT token is valid: ", user)
                print("===================================================================")
                return {"is_valid_jwt": True}
    print("User JWT token is invalid, and their credentials are: ", decoded_jwt)
    print("===================================================================")
    return HTTPException(status_code=401, detail="Invalid or Expired token, please login again!")

# Root or Home route.
@app.get("/")
def read_root():
    return {"msg": "Server is running!"}
# ===========================================================================================
# ===========================================================================================
# ===========================================================================================
