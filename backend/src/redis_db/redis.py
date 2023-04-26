# https://python-dependency-injector.ets-labs.org/examples/fastapi-redis.html

from src.config import host
import redis


redis_client = redis.Redis(host=host, port=6379, db=0)