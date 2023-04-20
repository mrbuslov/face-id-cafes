import asyncio
import os
from typing import Set, List

import cv2
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay, MediaBlackhole

from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import WebSocket

from src.face_id.schemas import Offer
from src.face_id.service import VideoTransformTrack
from src.face_id.utils.ws import VideoSocket

templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=templates_path)

pcs: Set[RTCPeerConnection] = set()
open_websockets: List[VideoSocket] = []


async def data_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        unique_id = await websocket.receive_text()
        open_websockets.append(VideoSocket(websocket=websocket, unique_id=unique_id))
        await websocket.send_text("Connection established")


async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def offer(params: Offer, request: Request) -> dict:
    peer_offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)
    recorder = MediaBlackhole()

    relay = MediaRelay()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            pc.addTrack(VideoTransformTrack(
                relay.subscribe(track),
                transform=params.video_transform,
                host=request.client.host,
                code=params.unique_id,
                websockets=open_websockets
                )
            )

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(peer_offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setRemoteDescription(peer_offer)
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


async def clear_peer_connections(peer_connections: Set[RTCPeerConnection] = pcs) -> None:
    # close peer connections
    coroutines = [pc.close() for pc in peer_connections]
    await asyncio.gather(*coroutines)
    pcs.clear()
