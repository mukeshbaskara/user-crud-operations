import json
import os
import base64

import requests
import redis
import yaml

from models.user_model import User

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6378')
REDIS_DB = os.environ.get('REDIS_DB', '0')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')

#ssl_context = ssl.create_default_context()

#ssl_context.load_verify_locations('/app/cert/redis-ca.pem')

"""
pool = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
    ssl_ca_certs='/app/cert/redis-ca.pem')
"""
"""
pool = redis.ConnectionPool(
    host='10.180.214.116',
    port=6378,
    db='test-redis',
    password='43095071-48a3-40f9-8252-9b4b7c0410b9',
    ssl=True,
    ssl_context=ssl_context)
"""


class RedisClient:

    def __init__(self):
        self.conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        #self.conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, ssl=True,
        #                              ssl_cert_reqs="none", ssl_ca_path='/app/cert/redis-ca.pem')

    def get(self, key: str):
        value = self.conn.get(f"user:{key}")
        if value is not None:
            try:
                return User.parse_obj(yaml.safe_load(value))
            except yaml.YAMLError as e:
                raise e
        else:
            return None

    def set(self, key: str, data: User):
        yaml_string = yaml.dump(data.dict())
        print(key)
        print(yaml_string)
        self.conn.set(f"user:{key}", yaml_string)

