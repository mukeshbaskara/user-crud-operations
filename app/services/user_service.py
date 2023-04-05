import requests
import os
import yaml
import io

from fastapi import HTTPException
from pydantic import ValidationError
import logging
from models.user_model import User
from repository.redis_client import RedisClient


ORDER_SERVICE = os.environ.get('ORDER_SERVICE', '')
ORDER_NAMESPACE = os.environ.get('ORDER_NAMESPACE', '')

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self):
        self.redis = RedisClient()

    def create_user(self, user: User):
        print('in user service create user')
        #self.redis.set(user.id, user.__dict__)

    def get_user(self, user_id: str):
        return self.redis.get(user_id)

    def get_orders(self, user_id: str):
        url = f"http://{ORDER_SERVICE}.{ORDER_NAMESPACE}.svc.cluster.local/order/list/{user_id}"
        print(url)
        response = requests.get(url)
        print(response)
        if response is not None:
            return response
        else:
            return None

    async def create_user_from_yaml(self, file):
        """
        Parse YAML data from an uploaded file and insert into redis
        """
        contents = await file.read()
        yaml_data = yaml.safe_load(io.StringIO(contents.decode('utf-8')))
        try:
            user = User(**yaml_data)
        except ValidationError as e:
            error_messages = [f"{error}" for error in e.errors()]
            raise HTTPException(status_code=400, detail={"error_messages": error_messages})
        self.redis.set(user.id, user)

