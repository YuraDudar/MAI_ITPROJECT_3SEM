# test_favorites.py
import pytest
from app.routes.favorites import router
from app.services.favorites_service import add_product_in_user_favorites, delete_product_in_user_favorites

@pytest.mark.asyncio
async def test_add_product_to_favorites(db_session):
    # Create a user and product
    from app.database.models import UserTable, RoleTable, ProductTable
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='testuser', email='testuser@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Add product to favorites
    added_product = await add_product_in_user_favorites(user.id, product.id, db_session)
    assert added_product == product.id

@pytest.mark.asyncio
async def test_delete_product_from_favorites(db_session):
    # Create a user and product
    from app.database.models import UserTable, RoleTable, ProductTable, FavoriteTable
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='testuser', email='testuser@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Add product to favorites
    favorite = FavoriteTable(user_id=user.id, product_id=product.id)
    db_session.add(favorite)
    await db_session.commit()

    # Delete product from favorites
    deleted_product = await delete_product_in_user_favorites(user.id, product.id, db_session)
    assert deleted_product.id == product.id