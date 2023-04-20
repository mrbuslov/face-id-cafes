# global configs
import os 
from starlette.templating import Jinja2Templates


# static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
# templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
# templates = Jinja2Templates(directory=templates_path)

static_dir = 'static'
templates_path = "templates"
templates = Jinja2Templates(directory=templates_path)