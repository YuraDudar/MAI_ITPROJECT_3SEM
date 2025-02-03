import time
from jose import jwt

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"

async def create_access_token(data: dict, minutes: int = 0) -> str:
    to_encode = data.copy()
    if minutes != 0:
        expire = time.time() + minutes * 60
    else:
        expire = time.time() + 900
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}