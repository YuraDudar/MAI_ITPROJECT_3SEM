from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from app.utils.jwt import decode_token

class AdminBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AdminBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request : Request):

        credentials: HTTPAuthorizationCredentials = await super(AdminBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt: str) -> bool:

        isTokenValid: bool = False

        try:
            payload = decode_token(jwt)
        except:
            payload = None

        if payload and payload["role"] == "admin":
            isTokenValid = True

        return isTokenValid

class SimpleBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(SimpleBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request : Request):

        credentials: HTTPAuthorizationCredentials = await super(SimpleBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt: str) -> bool:

        isTokenValid: bool = False

        try:
            payload = decode_token(jwt)
        except:
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid