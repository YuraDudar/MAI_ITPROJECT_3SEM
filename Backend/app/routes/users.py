from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.routes.schemas import RegRequest, UserUpdateRequest
from app.security import SimpleBearer
from app.services.user_service import (
    get_user_by_id,
    get_users_by_filters,
    create_new_user,
    update_user_by_id,
    delete_user_by_id
)
from app.utils.jwt import decode_token

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    token = credentials
    payload = await decode_token(token)
    user = await get_user_by_id(user_id, db)
    if not user:
        return {"detail": "User not found"}
    return user


@router.post("/users")
async def create_user(
        user: RegRequest,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    token = credentials
    payload = await decode_token(token)
    new_user = await create_new_user(user, db)
    return new_user


@router.put("/users/{user_id}")
async def update_user(
        user_id: int,
        user: UserUpdateRequest,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    token = credentials
    payload = await decode_token(token)

    if payload['user_id'] != user_id and payload['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    updated_user = await update_user_by_id(user_id, user, db)
    if not updated_user:
        return {"detail": "User not found"}
    return updated_user


@router.delete("/users/{user_id}")
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    token = credentials
    payload = await decode_token(token)
    if payload['user_id'] != user_id and payload['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    deleted_user = await delete_user_by_id(user_id, db)
    if not deleted_user:
        return {"detail": "User not found"}
    return deleted_user


@router.get("/users")
async def get_users(
        username: str = None,
        email: str = None,
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(SimpleBearer())
):
    users = await get_users_by_filters(db, username, email)
    return users
