import asyncio
from typing import Set, List

import cv2
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection
from src.face_id.schemas import CeleryResponse

from src.face_id.schemas import VideoSocket, UserData
from src.celery.worker import process_frame
from celery.result import AsyncResult

faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
pcs: Set[RTCPeerConnection] = set()


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
        self.celery_tasks_list = []

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
        print('frame received')
        # await asyncio.sleep(5)
        frame = await self.track.recv()

        for task_id in self.celery_tasks_list:
            task = await get_status(task_id)
            if task.is_ready:
                await self.notify_socket(task.task_result.user_name)
       
        if len(self.celery_tasks_list) <= 2:
            print('celery_tasks_list is less that 2')
            task = process_frame.delay()
            self.celery_tasks_list.append(task.id)


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


async def get_status(task_id: str) -> CeleryResponse:
    task_result = AsyncResult(task_id)
    result = CeleryResponse(
        task_id = task_id,
        task_status = task_result.status,
        task_result = UserData(**task_result.result),
        is_ready = task_result.ready()
    )
    print(result)
    return result