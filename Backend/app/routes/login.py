from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.routes.schemas import LoginRequest
from app.services.login_service import login_user

router = APIRouter()

@router.put("/login")
async def login(user: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login_user(user.email, user.password, db)