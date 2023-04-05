import uuid

import yaml
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.openapi.models import Response
from models.user_model import User
from services.user_service import UserService

user_router = APIRouter()
service = UserService()

logger = logging.getLogger(__name__)


@user_router.post("/user")
async def create_user(user: User):
    service.create_user(user)


@user_router.post("/user/create")
async def create_user_from_yaml(file: UploadFile = File(...)):
    print("in create user")
    try:
        await service.create_user_from_yaml(file)
        #return Response(content="User created successfully", status_code=200, media_type="application/json")
    except (ValueError, yaml.YAMLError, TypeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail="Failed to parse YAML data.")


@user_router.get("/user/get/{user_id}")
def get_user(user_id: str):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(404, "user not found")
    return user
    #return Response(content=user, status_code=200, media_type="application/json")


@user_router.get("/user/health")
def check_health():
    return 'im healthy'

