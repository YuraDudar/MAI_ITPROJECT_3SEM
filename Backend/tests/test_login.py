# test_login.py
import pytest
from passlib.context import CryptContext
from fastapi.testclient import TestClient
from app.routes.login import router
from app.services.login_service import login_user

@pytest.mark.asyncio
async def test_login_success(db_session):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    from app.database.models import UserTable, RoleTable
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    hashed_password = pwd_context.hash("password")  # Хэшируем пароль
    user = UserTable(username='testuser', email='testuser@example.com', password=hashed_password, role_id=role.id)
    db_session.add(user)
    await db_session.commit()

    response = await login_user('testuser@example.com', 'password', db_session)
    assert response.access_token
    assert response.token_type == 'Bearer'

@pytest.mark.asyncio
async def test_login_failure(db_session, mock_decode_token):
    response = await login_user('testuser@example.com', 'wrongpassword', db_session)
    assert response is None