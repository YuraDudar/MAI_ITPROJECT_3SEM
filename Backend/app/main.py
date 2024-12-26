from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import login, registration, cart, favorites, users, products, recommendation

api = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:37712"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(login.router)
api.include_router(registration.router)
api.include_router(users.router)
api.include_router(products.router)
api.include_router(recommendation.router)
api.include_router(cart.router)
api.include_router(favorites.router)

@api.options("/")
def options_root():
    return {"message": "OK"}
