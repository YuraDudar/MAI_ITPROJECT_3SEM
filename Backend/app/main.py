from fastapi import FastAPI
from app.routes import login, registration, cart, favorites

api = FastAPI()

api.include_router(login.router)
api.include_router(registration.router)
api.include_router(cart.router)
api.include_router(favorites.router)