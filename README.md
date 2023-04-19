# Server
- **RUN** - `uvicorn src.application:app --reload --port 80` (you have to be in backend folder)

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