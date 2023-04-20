from dataclasses import dataclass
from fastapi import WebSocket


@dataclass
class VideoSocket:
    """
    VideoSocket is a dataclass that holds the websocket, and it's unique_id
    """
    websocket: WebSocket
    unique_id: str
