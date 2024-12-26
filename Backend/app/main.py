from fastapi import FastAPI
from app.routes import login, registration, cart, favorites, users, products, recommendation

api = FastAPI()

api.include_router(login.router)
api.include_router(registration.router)
api.include_router(users.router)
api.include_router(products.router)
api.include_router(recommendation.router)
api.include_router(cart.router)
api.include_router(favorites.router)