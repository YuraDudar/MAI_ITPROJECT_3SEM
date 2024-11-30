from pydantic import BaseModel

class GetUserAnswer(BaseModel):
    id: int
    username: str
    email: str
    password: str
    role: str

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class GetProductAnswer(BaseModel):
    id: int
    name: str
    description: str
    price: float

class GetCartItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int