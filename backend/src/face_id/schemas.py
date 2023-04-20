from pydantic import BaseModel


class Offer(BaseModel):
    sdp: str
    type: str
    unique_id: str
    video_transform: str = None
