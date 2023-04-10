import yaml
import io
import logging
from redis.exceptions import RedisError, ConnectionError
from fastapi import HTTPException
from pydantic import ValidationError
from models.user_model import User
from repository.redis_client import RedisClient

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self):
        self.redis = RedisClient()

    def get_user(self, user_id: str):
        return self.redis.get(user_id)

    async def create_user_from_yaml(self, file):
        contents = await file.read()
        yaml_data = yaml.safe_load(io.StringIO(contents.decode('utf-8')))
        try:
            user = User(**yaml_data)
            result = self.redis.set(user.id, user)
            if result:
                return user.id
            else:
                raise HTTPException(status_code=500, detail={"Something went wrong, please check with support team"})
        except ValidationError as e:
            error_messages = [f"{error}" for error in e.errors()]
            logger.error(error_messages)
            raise HTTPException(status_code=400, detail={"error_messages": error_messages})
        except (RedisError, ConnectionError) as e:
            logger.error(f'Error: {e}')
            raise HTTPException(status_code=500, detail=e)

    async def update_user(self, user_id, file):
        contents = await file.read()
        yaml_data = yaml.safe_load(io.StringIO(contents.decode('utf-8')))
        try:
            if not self.redis.exists(user_id):
                return False
            user = User(**yaml_data)
            return self.redis.set(user_id, user)
        except ValidationError as e:
            error_messages = [f"{error}" for error in e.errors()]
            logger.error(error_messages)
            raise HTTPException(status_code=400, detail={"error_messages": error_messages})
        except (RedisError, ConnectionError) as e:
            logger.error(f'Error: {e}')
            raise HTTPException(status_code=500, detail=e)

    def delete_user(self, user_id: str):
        try:
            return self.redis.delete(user_id)
        except (RedisError, ConnectionError) as e:
            logger.error(f'Error: {e}')
            raise HTTPException(status_code=500, detail=e)
