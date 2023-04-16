FROM python:3.10

RUN apt-get update 

WORKDIR /var/backend

COPY backend/requirements.txt ./

RUN apt-get update \
    && apt-get install libpq-dev netcat libgl1 -y \
    && pip install -r requirements.txt 

COPY backend .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
