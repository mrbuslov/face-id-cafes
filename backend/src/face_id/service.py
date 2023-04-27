import asyncio
import json
import pickle
from typing import Set, List
import uuid

import cv2
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection
from src.face_id.schemas import CeleryResponse

from src.face_id.schemas import VideoSocket, UserData
from src.celery.worker import process_frame
from celery.result import AsyncResult
from src.config import MAX_IMG_PROCESS_SIMULTANEOUSLY
from src.redis_db.redis import redis_client

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
        print('ws notify block')
        print('websockets:', self.websockets)
        for ws in self.websockets:
            if ws.unique_id == self.code:
                print('ws found! sending data')
                await ws.websocket.send_json({
                    'status': 'detecting',
                    'code': self.code,
                    'name': name,
                })
                return {}

    async def recv(self):
        print('frame received')
        frame = await self.track.recv()

        # the error:  src.face_id.schemas.UserData() argument after ** must be a mapping, not NoneType. 
        # for now leave try except block
        try:
            for task_id in self.celery_tasks_list:
                task = await get_status(task_id)
                if task.is_ready:
                    # pass
                    print(task.task_result.user_name)
                    await self.notify_socket(task.task_result.user_name)
                    # self.celery_tasks_list.remove(task_id)
        except Exception as e:
            print('for task_id in self.celery_tasks_list exception: ', e)

       
        try:
            if len(self.celery_tasks_list) < MAX_IMG_PROCESS_SIMULTANEOUSLY:
                print('celery_tasks_list is less that 2')
                image_key = str(uuid.uuid4())

                '''
                Here're 2 options of converting the frame to bytes: 
                - using cv2.imencode
                - using pickle

                The second option allows to keep the size of the array, so it's more preferable
                '''
                frame_data = pickle.dumps(frame.to_ndarray(format="bgr24"))
                
                redis_client.set(image_key, frame_data)

                task = process_frame.delay(image_key)
                self.celery_tasks_list.append(task.id)
        except Exception as e:
            print(e)


        # just return user's video on front
        return frame



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
    print('get_status result', result)
    return result
