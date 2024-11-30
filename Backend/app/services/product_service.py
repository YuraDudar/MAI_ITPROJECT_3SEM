from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.contracs import GetProductAnswer
from app.database.models import ProductTable

async def get_product_by_id(id: int, db: AsyncSession) -> GetProductAnswer | None:

    stmt = select(ProductTable).filter(ProductTable.id==id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        return None

    return GetProductAnswer(id=id, name=product.name, description=product.description, price=product.price)