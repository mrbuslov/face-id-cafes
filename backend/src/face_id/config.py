# global configs
import os 
from starlette.templating import Jinja2Templates
# import redis
# import aioredis


# static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
# templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
# templates = Jinja2Templates(directory=templates_path)

static_dir = 'static'
templates_path = "templates"
templates = Jinja2Templates(directory=templates_path)
# create redis conn to keep websockets
# redis = aioredis.create_redis_pool("redis://127.0.0.1")