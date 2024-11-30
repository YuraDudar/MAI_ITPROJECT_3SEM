from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.contracs import GetProductAnswer, GetCartItem
from app.database.models import ShoppingCartTable
from app.services import product_service
from app.services.product_service import get_product_by_id


async def get_products_in_user_cart(user_id: int, db: AsyncSession) -> list:

    stmt = select(ShoppingCartTable).filter(ShoppingCartTable.user_id == user_id)
    result = await db.execute(stmt)
    products = result.scalars().all()

    returnList = []
    for product in products:
        pr = await get_product_by_id(product.product_id, db)
        returnList.append(GetCartItem(id=pr.id, name=pr.name, description=pr.description, price=pr.price, quantity=product.quantity))

    return returnList

async def get_product_in_user_cart(user_id: int, product_id: int, db: AsyncSession) -> GetCartItem | None:

    stmt = select(ShoppingCartTable).filter(ShoppingCartTable.user_id == user_id, ShoppingCartTable.product_id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is not None:
        pr = await get_product_by_id(product.product_id, db)
        return GetCartItem(id=pr.id, name=pr.name, description=pr.description, price=pr.price, quantity=product.quantity)

    return None

async def add_product_in_user_cart(user_id: int, product_id: int, db: AsyncSession) -> int:

    stmt = select(ShoppingCartTable).filter(ShoppingCartTable.user_id == user_id, ShoppingCartTable.product_id == product_id)
    result = await db.execute(stmt)
    product_user = result.scalar_one_or_none()

    if product_user is not None:
        stmt = update(ShoppingCartTable).where(ShoppingCartTable.user_id == user_id, ShoppingCartTable.product_id == product_id).values(user_id=product_user.user_id, product_id=product_user.product_id, quantity=product_user.quantity + 1)
        await db.execute(stmt)
        await db.commit()
    else:
        stmt = insert(ShoppingCartTable).values(user_id=user_id, product_id=product_id, quantity=1)
        await db.execute(stmt)
        await db.commit()

    return product_id

async def delete_product_in_user_cart(user_id: int, product_id: int, db: AsyncSession) -> GetProductAnswer | None:

    stmt = select(ShoppingCartTable).filter(ShoppingCartTable.user_id == user_id, ShoppingCartTable.product_id == product_id)
    result = await db.execute(stmt)
    product_user = result.scalar_one_or_none()

    if product_user is not None:
        if product_user.quantity == 1:
            stmt = delete(ShoppingCartTable).where(ShoppingCartTable.user_id == user_id, ShoppingCartTable.product_id == product_id)
            await db.execute(stmt)
            await db.commit()
        else:
            stmt = update(ShoppingCartTable).where(ShoppingCartTable.user_id == user_id,
                                                   ShoppingCartTable.product_id == product_id).values(
                user_id=product_user.user_id, product_id=product_user.product_id, quantity=product_user.quantity - 1)
            await db.execute(stmt)
            await db.commit()

    return await product_service.get_product_by_id(product_id, db)