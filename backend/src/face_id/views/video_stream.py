import asyncio
from typing import Set

import cv2
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay, MediaBlackhole

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.face_id.schemas import Offer
from src.face_id.service import VideoTransformTrack

faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

pcs: Set[RTCPeerConnection] = set()

templates = Jinja2Templates(directory="templates")


async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



async def offer(params: Offer):
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

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
                VideoTransformTrack(relay.subscribe(track), transform=params.video_transform)
            )


        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setRemoteDescription(offer)
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
