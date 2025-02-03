# test_registration.py
import pytest
from app.routes.registration import router
from app.services.reg_service import reg_user

@pytest.mark.asyncio
async def test_register_success(db_session):
    from app.routes.schemas import RegRequest
    from app.database.models import RoleTable
    # Создаем роль
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()

    # Регистрируем пользователя
    request = RegRequest(username='newuser', email='newuser@example.com', password='password')
    user = await reg_user(request.username, request.email, request.password, db_session)
    assert user.username == 'newuser'

@pytest.mark.asyncio
async def test_register_existing_email(db_session):
    # Create a user
    from app.database.models import UserTable, RoleTable
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='existinguser', email='existing@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    await db_session.commit()

    # Attempt to register with the same email
    request = {'username': 'newuser', 'email': 'existing@example.com', 'password': 'password'}
    user = await reg_user(**request, db=db_session)
    assert user is None