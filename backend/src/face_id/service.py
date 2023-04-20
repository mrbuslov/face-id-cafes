import asyncio
from typing import Set, List

import cv2
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay, MediaBlackhole

from starlette.templating import Jinja2Templates

from src.face_id.utils.ws import VideoSocket

faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
pcs: Set[RTCPeerConnection] = set()
templates = Jinja2Templates(directory="templates")


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform, host: str, code: str, websockets: List[VideoSocket]):
        super().__init__()
        self.track = track
        self.transform = transform
        self.host = host
        self.code = code
        self.websockets = websockets

    async def notify_socket(self, name:str = None) -> dict:
        for ws in self.websockets:
            if ws.unique_id == self.code:
                await ws.websocket.send_json({
                    'status': 'detecting',
                    'code': self.code,
                    'name': name,
                })
                return {}

    async def recv(self):
        # await asyncio.sleep(5)
        frame = await self.track.recv()
        await self.notify_socket()

        img = frame.to_ndarray(format="bgr24")
        # https://stackoverflow.com/a/55628240
        face = faces.detectMultiScale(img, 1.1, 6)
        # face = faces.detectMultiScale(img, scaleFactor=1.5, minNeighbors=1) # higher speed, worse quality
        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame


async def clear_peer_connections(peer_connections: Set[RTCPeerConnection]) -> None:
    # close peer connections
    coroutines = [pc.close() for pc in peer_connections]
    await asyncio.gather(*coroutines)
    pcs.clear()
