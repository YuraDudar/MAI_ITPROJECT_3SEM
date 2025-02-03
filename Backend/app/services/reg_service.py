from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import create_new_user
from app.services.user_service import get_user_by_email
from app.services.contracs import CreateUserRequest
from app.services.contracs import GetUserAnswer


async def reg_user(username: str, email: str, password: str, db: AsyncSession) -> GetUserAnswer | None:

    if await get_user_by_email(email, db) is not None:
        return None

    await create_new_user(CreateUserRequest(username=username, email=email, password=password), db)
    return await get_user_by_email(email, db)