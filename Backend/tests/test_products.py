# test_products.py
import pytest
from app.routes.products import router
from app.services.product_service import create_new_product, get_product_by_id, update_product_by_id, delete_product_by_id

@pytest.mark.asyncio
async def test_create_product(db_session):
    from app.routes.schemas import ProductRequest
    request = ProductRequest(name='Test Product', description='A test product', price=10.99)  # Используем Pydantic модель
    product = await create_new_product(request, db_session)
    assert product.name == 'Test Product'

@pytest.mark.asyncio
async def test_get_product(db_session):
    # Create a product
    from app.database.models import ProductTable
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Get the product
    product = await get_product_by_id(1, db_session)
    assert product.id == 1
    assert product.name == 'Test Product'

@pytest.mark.asyncio
async def test_update_product(db_session):
    from app.routes.schemas import ProductRequest
    from app.database.models import ProductTable
    # Создаем продукт
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Обновляем продукт
    request = ProductRequest(name='Updated Product', description='Updated description', price=15.99)  # Используем Pydantic модель
    updated_product = await update_product_by_id(product.id, request, db_session)
    assert updated_product.name == 'Updated Product'

@pytest.mark.asyncio
async def test_delete_product(db_session):
    # Create a product
    from app.database.models import ProductTable
    product = ProductTable(name='Test Product', description='A test product', price=10.99)
    db_session.add(product)
    await db_session.commit()

    # Delete the product
    deleted_product = await delete_product_by_id(1, db_session)
    assert deleted_product.id == 1