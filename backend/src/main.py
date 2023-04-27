import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.utils import (
    update_http_routes,
    update_websocket_routes,
    update_events,
    catch_exceptions_middleware,
)
from src.face_id.routes import routes as face_id_routes, web_socket_routes, events
from src.config import static_dir, host
from src.redis_db.redis import redis_client


ROOT = os.path.dirname(__file__)
app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app = update_http_routes(app, face_id_routes)
app = update_websocket_routes(app, web_socket_routes)
app = update_events(app, events)
app.middleware('http')(catch_exceptions_middleware)



@app.on_event("shutdown")
def shutdown_event():
    print('app shutdown!!!!!!!!!!!')
    try:
        redis_client.flushdb()
    except Exception as e:
        print('shutdown exception', e)


if __name__ == "__main__":
    # ssl_key = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "certs/key.pem")
    # ssl_crt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "certs/cert.pem")
    ssl_key = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "certs/server.key")
    ssl_crt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "certs/server.crt")
    
    uvicorn.run(
        app,
        # host="0.0.0.0",
        host=host,
        port=8000,
        ssl_keyfile=ssl_key,
        ssl_certfile=ssl_crt,
    )
