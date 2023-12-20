import os


ACCESS_TOKEN_ALIVE = int(os.environ.get('ACCESS_TOKEN_ALIVE')) 
REFRESH_TOKEN_ALIVE = int(os.environ.get('REFRESH_TOKEN_ALIVE'))
SECRET_KEY = os.environ.get('SECRET_KEY')