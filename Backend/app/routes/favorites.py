from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.security import SimpleBearer
from app.utils.jwt import decode_token
from app.services.favorites_service import get_favorite_products_by_user, get_product_in_user_favorites, add_product_in_user_favorites, delete_product_in_user_favorites

router = APIRouter()

@router.get("/favorites")
async def get_all_favorite_products(db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await get_favorite_products_by_user(payload["user_id"], db)

@router.get("/favorites/{id}")
async def get_product_in_favorites(id: int, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await get_product_in_user_favorites(payload['user_id'], id, db)

@router.post("/favorites")
async def add_product_in_favorites(id: int, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await add_product_in_user_favorites(payload['user_id'], id, db)

@router.delete("/favorites/{id}")
async def delete_product_in_favorites(id: int, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await delete_product_in_user_favorites(payload["user_id"], id, db)