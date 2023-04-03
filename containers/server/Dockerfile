FROM python:3.10

RUN apt-get update 

WORKDIR /var/backend

COPY backend/requirements.txt ./

RUN apt-get update \
    && apt-get install libpq-dev netcat -y \
    && pip install -r requirements.txt 

COPY backend .
