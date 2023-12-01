

import datetime
import time
import jwt 
from decouple import config

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')

def token_response(token: str,user_id : str):
    return {
        'jwt_token': token,
        'email' : user_id
    }

def signJWT(user_id: str):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
    payload = {
        'email': user_id,
        'expires': expiration_time.timestamp()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token,user_id)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token,JWT_SECRET,algorithm=JWT_ALGORITHM)
        current_time = time.time()
        delta_time = decode_token['expires'] - current_time
        if delta_time > 0:
            print("token will expire after : ",delta_time)
            return decode_token
        print("token has expired : ",delta_time)
        return  {}
    except:
        return {}