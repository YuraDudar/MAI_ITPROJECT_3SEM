from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.contracs import GetProductAnswer
from app.database.models import ProductTable
from app.routes.schemas import ProductRequest


async def get_product_by_id(id: int, db: AsyncSession) -> GetProductAnswer | None:

    stmt = select(ProductTable).filter(ProductTable.id==id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        return None

    return GetProductAnswer(id=id, name=product.name, description=product.description, price=product.price)

async def get_product_by_filter(name: str, db: AsyncSession) -> list[GetProductAnswer] | None:

    stmt = select(ProductTable).filter(ProductTable.name.ilike(f"%{name}%"))

    result = await db.execute(stmt)
    products = result.scalars().all()

    if products is None:
        return None

    products_answer = []
    for row in products:
        products_answer.append(GetProductAnswer(id=row.id, name=row.name, description=row.description, price=row.price))
    return products_answer

async def create_new_product(request: ProductRequest, db: AsyncSession):

    stmt = insert(ProductTable).values(name=request.name, description=request.description, price=request.price)
    result = await db.execute(stmt)
    await db.commit()
    return await get_product_by_id(result.inserted_primary_key[0], db)

async def update_product_by_id(product_id: int, request: ProductRequest, db: AsyncSession):

    stmt = select(ProductTable).filter(ProductTable.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="User not found")

    product.id = product_id
    product.name = request.name
    product.description = request.description
    product.price = request.price

    await db.commit()
    return GetProductAnswer(id=product_id, name=product.name, description=product.description, price=product.price)

async def delete_product_by_id(product_id: int, db: AsyncSession):

    stmt = select(ProductTable).filter(ProductTable.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        return {"detail": "Product not found"}

    await db.delete(product)
    await db.commit()
    return product
