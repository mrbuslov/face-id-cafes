import dataclasses
import os
import pickle
import time
from celery import Celery
from src.face_id.schemas import UserData
import cv2
from av import VideoFrame
import numpy as np
import json
from celery.exceptions import SoftTimeLimitExceeded
from src.config import host
from src.redis_db.redis import redis_client
import redis

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', f"redis://{host}:6379")
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', f"redis://{host}:6379")
redis_client = redis.Redis(host=host, port=6379, db=0)


faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
@celery.task(name='process_frame', time_limit=7)
def process_frame(img_id: str):
    try:
        frame = pickle.loads(redis_client.get(img_id))

        # https://stackoverflow.com/a/55628240
        face = faces.detectMultiScale(frame, 1.05, 18)

        try:
            for (x, y, w, h) in face:
                # crop face from image
                cropped_face = frame[y:y + h, x:x + w]

            cv2.imwrite('cropped_face.jpg', cropped_face)
            redis_client.delete(img_id)
        except Exception as e:
            print('process_frame exception: (NO FACE DETECTED)')
            # raise Exception('NO FACE DETECTED')

        return dataclasses.asdict(UserData(user_name='Dmitry'))

    except SoftTimeLimitExceeded:
        return dataclasses.asdict(UserData(user_name='Celery worker time out'))
