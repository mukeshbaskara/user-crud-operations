import yaml
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from models.user_model import User
from services.user_service import UserService

user_router = APIRouter()
service = UserService()

logger = logging.getLogger(__name__)


@user_router.post("/user")
async def create_user_from_yaml(file: UploadFile = File(...)):
    try:
        user_id = await service.create_user_from_yaml(file)
    except (ValueError, yaml.YAMLError, TypeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail="Failed to parse YAML data.")
    return JSONResponse(
        status_code=200,
        content={"message": "user created successfully", "id": user_id}
    )


@user_router.put("/user/{user_id}")
async def update_user_from_yaml(user_id: str, file: UploadFile = File(...)):
    try:
        result = await service.update_user(user_id, file)
        if result:
            return JSONResponse(
                status_code=200,
                content={"message": f"updated user:{user_id} in Redis."}
            )
        else:
            return JSONResponse(
                status_code=404,
                content={"message": f"User:{user_id} not found in Redis."}
            )
    except (ValueError, yaml.YAMLError, TypeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail="Failed to parse YAML data.")


@user_router.delete("/user/{user_id}")
def delete_user(user_id: str):
    result = service.delete_user(user_id)
    if result == 1:
        return JSONResponse(
            status_code=200,
            content={"message": f"Deleted user:{user_id} from Redis."}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": f"User:{user_id} not found in Redis."}
        )


@user_router.get("/user/{user_id}")
def get_user(user_id: str):
    print("in get user request handler")
    print(user_id)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return JSONResponse(
        status_code=200,
        content={"user": user.json()}
    )


@user_router.get("/health")
def check_health():
    return 'im healthy'
