from fastapi import Depends
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import UserTable, RoleTable

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: str
    password: str
    role: str

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:

    stmt = select(UserTable).filter(UserTable.email == email)
    result = await db.execute(stmt)
    user = result.scalar()

    if user is None:
        return None

    stmt = select(RoleTable).filter(RoleTable.id == user.role_id)
    result = await db.execute(stmt)
    role = result.scalar()

    return User(username=user.username, email=user.email, password=user.password, role=role.role)

async def create_new_user(username: str, email:str, password: str, db: AsyncSession):

    stmt = insert(UserTable).values(username=username, email=email, password=pwd_context.hash(password), role_id=0)
    await db.execute(stmt)
    await db.commit()