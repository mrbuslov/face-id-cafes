from .face_id.service import clear_peer_connections
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path


ROOT = os.path.dirname(__file__)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("shutdown")
async def on_shutdown():
    clear_peer_connections()



app.add_api_route(path='/', endpoint=index)
app.add_api_route(path='/offer', endpoint=offer, methods=['post'])
