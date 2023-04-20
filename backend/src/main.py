import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.face_id.utils.utils import update_http_routes, update_websocket_routes, update_events
from src.face_id.routes import routes as face_id_routes, web_socket_routes, events

ROOT = os.path.dirname(__file__)
app = FastAPI()

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app = update_http_routes(app, face_id_routes)
app = update_websocket_routes(app, web_socket_routes)
app = update_events(app, events)

if __name__ == "__main__":
    ssl_key = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "certs/key.pem")
    ssl_crt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "certs/cert.pem")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile=ssl_key,
        ssl_certfile=ssl_crt
    )
