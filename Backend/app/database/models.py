from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RoleTable(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(255), nullable=False)

class UserTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='SET NULL'), nullable=True)

class ProductTable(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)

class ShoppingCartTable(Base):
    __tablename__ = 'shopping_cart'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)

class FavoriteTable(Base):
    __tablename__ = 'favorites'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)