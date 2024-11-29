from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import create_new_user
from app.services.user_service import User, get_user_by_email

async def reg_user(username: str, email: str, password: str, db: AsyncSession) -> User | None:

    if await get_user_by_email(email, db) is not None:
        return None

    await create_new_user(username, email, password, db)
    return await get_user_by_email(email, db)