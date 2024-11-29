from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.services.login_service import login_user
from app.services.reg_service import reg_user

api = FastAPI()

class UserLogin(BaseModel):
    email: str
    password: str

class UserReg(BaseModel):
    email: str
    username: str
    password: str

@api.put("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(user.email, user.password, db)

@api.post("/register")
async def reg(user: UserReg, db: AsyncSession = Depends(get_db)):
    return await reg_user(user.username, user.email, user.password, db)