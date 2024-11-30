from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.contracs import GetProductAnswer
from app.database.models import FavoriteTable
from app.services import product_service
from app.services.product_service import get_product_by_id


async def get_favorite_products_by_user(user_id: int, db: AsyncSession) -> list:

    stmt = select(FavoriteTable.product_id).filter(FavoriteTable.user_id == user_id)
    result = await db.execute(stmt)
    product_ids = result.scalars().all()

    returnList = []
    for product_id in product_ids:
        returnList.append(await product_service.get_product_by_id(product_id, db))

    return returnList

async def get_product_in_user_favorites(user_id: int, product_id: int, db: AsyncSession) -> GetProductAnswer | None:

    stmt = select(FavoriteTable).filter(FavoriteTable.user_id == user_id, FavoriteTable.product_id == product_id)
    result = await db.execute(stmt)
    product_user = result.scalar_one_or_none()

    if product_user is not None:
        return await get_product_by_id(product_user.product_id, db)
    else:
        return None

async def add_product_in_user_favorites(user_id: int, product_id: int, db: AsyncSession) -> int:

    stmt = select(FavoriteTable.product_id).filter(FavoriteTable.user_id == user_id)
    result = await db.execute(stmt)
    product_ids = result.scalars().all()

    if product_id not in product_ids:
        stmt = insert(FavoriteTable).values(user_id=user_id, product_id=product_id)
        await db.execute(stmt)
        await db.commit()

    return product_id

async def delete_product_in_user_favorites(user_id: int, product_id: int, db: AsyncSession) -> GetProductAnswer | None:

    stmt = select(FavoriteTable.product_id).filter(FavoriteTable.user_id == user_id)
    result = await db.execute(stmt)
    product_ids = result.scalars().all()

    if product_id in product_ids:
        stmt = delete(FavoriteTable).where(FavoriteTable.user_id == user_id, FavoriteTable.product_id == product_id)
        await db.execute(stmt)
        await db.commit()
    else:
        return None

    return await product_service.get_product_by_id(product_id, db)