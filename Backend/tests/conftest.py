import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
from app.database.database import get_db
from fastapi.testclient import TestClient
from app.main import api
from app.security import SimpleBearer
from app.utils.jwt import decode_token

@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session(db_engine):
    async_session = sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)
    session = async_session()
    yield session
    await session.close()

@pytest_asyncio.fixture
def override_get_db(db_session):
    async def _override_get_db():
        yield db_session
    return _override_get_db

@pytest_asyncio.fixture
def client(override_get_db, monkeypatch):
    monkeypatch.setattr('app.database.database.get_db', override_get_db)
    with TestClient(api) as c:
        yield c

@pytest_asyncio.fixture
def mock_decode_token(mocker):
    mock = mocker.patch('app.utils.jwt.decode_token')
    mock.return_value = {'sub': 'testuser@example.com', 'role': 'user', 'user_id': 1}
    return mock

@pytest_asyncio.fixture
def auth_client(client, mock_decode_token):
    client.headers = {
        'Authorization': 'Bearer valid-token'
    }
    return client