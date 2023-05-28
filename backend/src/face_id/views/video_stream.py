import asyncio
import base64
import json
import os
from typing import Set, List

import cv2
from av import VideoFrame
import easyocr # https://www.jaided.ai/easyocr/

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay, MediaBlackhole

from starlette.requests import Request
from fastapi import WebSocket

from src.face_id.schemas import Offer
from src.face_id.service import VideoTransformTrack
from src.face_id.schemas import VideoSocket
from src.config import templates


pcs: Set[RTCPeerConnection] = set()
# TODO: keep all websockets in redis db
open_websockets: List[VideoSocket] = []


async def data_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        unique_id = await websocket.receive_text()
        open_websockets.append(VideoSocket(websocket=websocket, unique_id=unique_id))
        await websocket.send_json({'status':'connection_established'})


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
            pc.addTrack(
                VideoTransformTrack(
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


async def screenshot(request: Request):
    res = await request.json()
    
    base64_code = res.get('screenshot')
    img_data = base64_code.encode()
    content = base64.b64decode(img_data)

    reader = easyocr.Reader(['ru', 'en', 'uk'])
    result = reader.readtext(content, detail=0, paragraph=True)
    print(' '.join(result))

    return 'ok'