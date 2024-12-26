from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.security import SimpleBearer
from app.utils.jwt import decode_token
from app.routes.schemas import ProductRequest
from app.services.product_service import get_product_by_id, get_product_by_filter, create_new_product, update_product_by_id, \
    delete_product_by_id

router = APIRouter()

@router.get("/products/{product_id}")
async def get_product(
        product_id: int,
        db: AsyncSession = Depends(get_db)
        # ,credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    product = await get_product_by_id(product_id, db)
    if not product:
        return {"detail": "Product not found"}
    return product

@router.get("/products")
async def get_product_by_name(
        name: str = None,
        db: AsyncSession = Depends(get_db)
        # ,credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    products = await get_product_by_filter(name, db)
    if not products:
        return {"detail": "Products not found"}
    return products

@router.post("/products")
async def create_product(
        user: ProductRequest,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    token = credentials
    payload = await decode_token(token)
    new_product = await create_new_product(user, db)
    if not new_product:
        return {"detail": "Product not created"}
    return new_product

@router.put("/products/{product_id}")
async def update_product(
        product_id: int,
        product: ProductRequest,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    token = credentials
    payload = await decode_token(token)

    updated_product = await update_product_by_id(product_id, product, db)
    if not updated_product:
        return {"detail": "Product not found"}
    return updated_product

@router.delete("/products/{product_id}")
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    token = credentials
    payload = await decode_token(token)

    product = await delete_product_by_id(product_id, db)
    if not product:
        return {"detail": "Product not found"}
    return product
