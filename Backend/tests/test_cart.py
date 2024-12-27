# test_cart.py
import pytest
from app.routes.cart import router
from app.services.cart_service import add_product_in_user_cart, delete_product_in_user_cart

@pytest.mark.asyncio
async def test_add_product_to_cart(db_session):
    from app.database.models import UserTable, RoleTable, ProductTable
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='testuser', email='testuser@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Create a product
    from app.database.models import ProductTable
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Add product to cart
    added_product = await add_product_in_user_cart(user.id, product.id, db_session)
    assert added_product == product.id

@pytest.mark.asyncio
async def test_delete_product_from_cart(db_session):
    # Create a user and product
    from app.database.models import UserTable, RoleTable, ProductTable, ShoppingCartTable
    role = RoleTable(role='user')
    db_session.add(role)
    await db_session.flush()
    user = UserTable(username='testuser', email='testuser@example.com', password='hashedpassword', role_id=role.id)
    db_session.add(user)
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Add product to cart
    cart_item = ShoppingCartTable(user_id=user.id, product_id=product.id, quantity=1)
    db_session.add(cart_item)
    await db_session.commit()

    # Delete product from cart
    deleted_product = await delete_product_in_user_cart(user.id, product.id, db_session)
    assert deleted_product.id == product.id