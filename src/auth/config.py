import os


ACCESS_TOKEN_ALIVE = int(os.environ.get('ACCESS_TOKEN_ALIVE', 5)) 
REFRESH_TOKEN_ALIVE = int(os.environ.get('REFRESH_TOKEN_ALIVE', 7))
SECRET_KEY = os.environ.get('SECRET_KEY')
SERVER_SECRET_KEY = os.environ.get('SERVER_SECRET_KEY')