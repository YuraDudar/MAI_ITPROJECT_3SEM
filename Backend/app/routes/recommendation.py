from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

import ml_solution.rec_sys as rec_sys
from app.database.database import get_db
from app.security import SimpleBearer
from app.utils.jwt import decode_token

router = APIRouter()


@router.get("/recommendation", response_model=list[int])
async def get_recommendation(quantity:int = 5, db: AsyncSession = Depends(get_db),
                             credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
                             ):
    token = credentials
    payload = await decode_token(token)
    user_id = payload["user_id"]

    recommended_products = rec_sys.get_rec(user_id, quantity)
    return recommended_products
