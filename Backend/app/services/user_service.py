from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserTable, RoleTable
from app.services.contracs import GetUserAnswer, CreateUserRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(email: str, db: AsyncSession) -> GetUserAnswer | None:

    stmt = select(UserTable).filter(UserTable.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        return None

    stmt = select(RoleTable).filter(RoleTable.id == user.role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()

    return GetUserAnswer(id=user.id, username=user.username, email=user.email, password=user.password, role=role.role)

async def create_new_user(request: CreateUserRequest, db: AsyncSession):

    stmt = insert(UserTable).values(username=request.username, email=request.email, password=pwd_context.hash(request.password), role_id=0)
    await db.execute(stmt)
    await db.commit()