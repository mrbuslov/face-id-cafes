import dataclasses
import os
import time
from celery import Celery
from src.face_id.schemas import UserData

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', "redis://127.0.0.1:6379")
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', "redis://127.0.0.1:6379")


@celery.task(name='process_frame')
def process_frame():
    print(dataclasses.asdict(UserData(user_name='Dmitry')))
    return dataclasses.asdict(UserData(user_name='Dmitry'))
