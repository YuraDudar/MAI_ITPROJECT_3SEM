from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str

class RegRequest(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserUpdateRequest(BaseModel):
    email: str
    username: str
    password: str

class ProductRequest(BaseModel):
    name: str
    description: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
