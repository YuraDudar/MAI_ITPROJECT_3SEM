from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.security import SimpleBearer
from app.utils.jwt import decode_token
from app.services.cart_service import get_products_in_user_cart, get_product_in_user_cart, add_product_in_user_cart, delete_product_in_user_cart

router = APIRouter()

@router.get("/cart")
async def get_all_products_in_cart(db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await get_products_in_user_cart(payload["user_id"], db)

@router.get("/cart/{id}")
async def get_product_in_cart(id: int, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await get_product_in_user_cart(payload['user_id'], id, db)

@router.post("/cart")
async def add_product_in_cart(id: int, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await add_product_in_user_cart(payload['user_id'], id, db)

@router.delete("/cart/{id}")
async def delete_product_in_cart(id: int, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())):
    token = credentials
    payload = await decode_token(token)
    return await delete_product_in_user_cart(payload["user_id"], id, db)