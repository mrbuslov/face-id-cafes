# Server
- **RUN** - `uvicorn src.main:app --reload --port 8000 --host 127.0.0.1` (you have to be in backend folder)
- **Run celery locally** (you have to be in backend folder)  
  - Windows: `celery -A src.celery.worker.celery worker --loglevel=info --logfile=logs/celery/celery.log -P gevent` 
  - Others: `celery -A src.celery.worker.celery worker --loglevel=info --logfile=logs/celery/celery.log`


# Linters

***Note***: if you want to run linters, go to directory - it can be either *backend* or *frontend*  
Be sure to run the backend if you want to "linter" it.  
- **Backend**: 
  - `python flake8`  
  Runs flake8 (django version). Changes you should make *by yourself*.
  - `python black .`  
  Changes files due to PEP8 style using black library.   
- **Frontend**:
  - `npm run lint:styles`  
  Runs style linter in the terminal. You'll see the errors, connected with code style in *.css* files.
  - `npm run lint:styles:fix`  
    Fixes majority of style errors. There may be some error, that you have to fix *by yourself*.


# Desktop
- Generate an app: `nativefier --name "Face-ID" http://127.0.0.1:8000/`


# Alembic 

### Migrations
- Make migrations `alembic revision --autogenerate -m "MIGRATION_NAME"`
- Migrate `alembic upgrade head` or `alembic upgrade MIGRATION_HASH`

### Tutorial
- Watch [this video](https://www.youtube.com/watch?v=eXj1gdDLKho&ab_channel=FastAPIChannel)


# Desktop (Electron)

- Run `npm start`