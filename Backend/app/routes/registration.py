from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.routes.schemas import RegRequest
from app.services.reg_service import reg_user

router = APIRouter()

@router.post("/register")
async def reg(user: RegRequest, db: AsyncSession = Depends(get_db)):
    return await reg_user(user.username, user.email, user.password, db)