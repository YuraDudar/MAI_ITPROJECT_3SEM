from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.jwt import create_access_token
from app.services.user_service import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(hashed_password: str, password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

async def login_user(email: str, password: str, db: AsyncSession) -> Token | None:

    user = await get_user_by_email(email, db)
    if user is None or not authenticate_user(user.password, password):
        return None

    token = await create_access_token({"sub": user.email})
    return Token(access_token=token, token_type="bearer")