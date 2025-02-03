# test_users.py
import pytest
from app.routes.users import router
from app.services.user_service import get_user_by_id, update_user_by_id, delete_user_by_id
from app.database.models import RoleTable
from app.database.models import UserTable

@pytest.mark.asyncio
async def test_get_user(db_session):
    # Create a user
    from app.database.models import UserTable, RoleTable
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='testuser', email='testuser@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    await db_session.commit()

    # Get the user
    retrieved_user = await get_user_by_id(user.id, db_session)
    assert retrieved_user.id == user.id
    assert retrieved_user.username == 'testuser'

@pytest.mark.asyncio
async def test_update_user(db_session):
    from app.routes.schemas import UserUpdateRequest
    # Создаем пользователя
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='testuser', email='testuser@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    await db_session.commit()

    # Обновляем пользователя
    request = UserUpdateRequest(username='updateduser', email='updateduser@example.com', password='newpassword')  # Используем Pydantic модель
    updated_user = await update_user_by_id(user.id, request, db_session)
    assert updated_user.username == 'updateduser'

@pytest.mark.asyncio
async def test_delete_user(db_session):
    # Создаем пользователя
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='testuser', email='testuser@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    await db_session.commit()

    # Удаляем пользователя
    response = await delete_user_by_id(user.id, db_session)
    
    # Проверяем, что функция вернула ожидаемый словарь
    assert response == {"detail": "User deleted successfully"}