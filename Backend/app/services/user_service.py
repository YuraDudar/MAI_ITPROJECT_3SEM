from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserTable, RoleTable
from app.services.contracs import GetUserAnswer, CreateUserRequest
from app.routes.schemas import UserUpdateRequest
from app.utils.jwt import decode_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_id(id: int, db: AsyncSession) -> GetUserAnswer | None:

    stmt = select(UserTable).filter(UserTable.id == id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        return None

    stmt = select(RoleTable).filter(RoleTable.id == user.role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()

    return GetUserAnswer(id=user.id, username=user.username, email=user.email, password=user.password, role=role.role)

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

    stmt = insert(UserTable).values(username=request.username, email=request.email, password=pwd_context.hash(request.password), role_id=1)
    await db.execute(stmt)
    await db.commit()

async def update_user_by_id(user_id: int, request: UserUpdateRequest, db: AsyncSession):

    stmt = select(UserTable).filter(UserTable.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    stmt = select(RoleTable).filter(RoleTable.id == user.role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()

    user.username = request.username
    user.email = request.email
    user.password = pwd_context.hash(request.password)

    await db.commit()
    return GetUserAnswer(id=user.id, username=user.username, email=user.email, password=user.password, role=role.role)


async def delete_user_by_id(id: int, db: AsyncSession):

    stmt = select(UserTable).filter(UserTable.id == id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted successfully"}

async def get_users_by_filters(db: AsyncSession, username: str = None, email: str = None):

    stmt = select(UserTable).join(RoleTable, RoleTable.id == UserTable.role_id)

    if username:
        stmt = stmt.filter(UserTable.username.ilike(f"%{username}%"))
    if email:
        stmt = stmt.filter(UserTable.email.ilike(f"%{email}%"))

    result = await db.execute(stmt)
    users = result.scalars().all()

    users_answer = []
    for user in users:
        role_stmt = select(RoleTable).filter(RoleTable.id == user.role_id)
        role_result = await db.execute(role_stmt)
        role = role_result.scalar_one_or_none()
        users_answer.append(GetUserAnswer(id=user.id, username=user.username, email=user.email, password=user.password, role=role.role))

    return users_answer
