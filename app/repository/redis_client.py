import os
import redis
import yaml
from models.user_model import User

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB = os.environ.get('REDIS_DB', '0')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'None')
REDIS_MAX_CON = os.environ.get('REDIS_MAX_CONNECTIONS', '1000')


class RedisConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance.redis_pool = redis.ConnectionPool(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                max_connections=int(REDIS_MAX_CON)
            )
        return cls._instance

    def get_redis_client(self):
        return redis.Redis(connection_pool=self.redis_pool)


class RedisClient:

    def __init__(self):
        self.conn = RedisConnection().get_redis_client()

    def get(self, key: str):
        with self.conn as conn:
            value = conn.get(f"user:{key}")
            if value is not None:
                try:
                    return User.parse_obj(yaml.safe_load(value))
                except yaml.YAMLError as e:
                    raise e
            else:
                return None

    def exists(self, key: str):
        with self.conn as conn:
            return conn.exists(f"user:{key}")

    def set(self, key: str, data: User):
        yaml_string = yaml.dump(data.dict())
        with self.conn as conn:
            return conn.set(f"user:{key}", yaml_string)

    def delete(self, key: str):
        with self.conn as conn:
            return conn.delete(f"user:{key}")
