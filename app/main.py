from fastapi import FastAPI
from routers.user_router import user_router

fastapi = FastAPI()

fastapi.include_router(user_router)
