from pydantic import BaseModel
from dataclasses import dataclass
from fastapi import WebSocket


class Offer(BaseModel):
    sdp: str
    type: str
    unique_id: str
    video_transform: str = None


@dataclass
class VideoSocket:
    """
    VideoSocket is a dataclass that holds the websocket, and it's unique_id
    """
    websocket: WebSocket
    unique_id: str


@dataclass
class UserData:
    '''
    Class, that represents user data
    '''
    user_name: str


@dataclass
class CeleryResponse:
    '''
    Class, that represents response from celery get_status function (status of celery task)
    '''
    task_id: str
    task_status: str
    task_result: UserData
    is_ready: bool



# @dataclass 
# class CeleryFrame