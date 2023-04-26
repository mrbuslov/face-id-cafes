# global configs
import os 
from starlette.templating import Jinja2Templates
from typing import AsyncIterator
import redis


# static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
# templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
# templates = Jinja2Templates(directory=templates_path)

host = '127.0.0.1'

static_dir = 'static'
templates_path = "templates"
templates = Jinja2Templates(directory=templates_path)

MAX_IMG_PROCESS_SIMULTANEOUSLY = 2

