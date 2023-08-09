


from fastapi import Request , HTTPException
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT




class jwt_bearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(jwt_bearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            jwt_bearer, self
        ).__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme"
                )
            
            if not self.validate_token(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid credentials"
                )
                
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid credentials"
            )

    def validate_token(self, token: str):
        payload = decodeJWT(token)
        isTokenValid = False  # Initialize with False
        if payload:
            print(payload)
            isTokenValid = True  # Set to True if payload is not None
        return isTokenValid  # Return the value, not the comparison
