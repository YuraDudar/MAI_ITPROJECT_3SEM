from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, relationship

DATABASE_URL = "postgresql+asyncpg://user:secret@localhost:5432/db"

engine = create_async_engine(DATABASE_URL, echo=True)

metadata = MetaData()

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session

Base = declarative_base()

class RoleTable(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(255), nullable=False)

    users = relationship("UserTable", back_populates="role", passive_deletes=True)


class UserTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='SET NULL'), nullable=True)

    role = relationship("RoleTable", back_populates="users")