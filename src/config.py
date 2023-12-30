import os
from pathlib import Path
from typing import List
from pydantic import AnyHttpUrl, TypeAdapter
from dotenv import load_dotenv


load_dotenv()

def validate_backend_cors_origins():
    origins = os.environ.get('BACKEND_CORS_ORIGINS')
    ta = TypeAdapter(List[AnyHttpUrl])
    return ta.validate_python(origins.split(','))

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

BASE_DIR = Path.cwd()
UPLOADS_DIR = Path(BASE_DIR, 'uploads')
AVATARS_DIR = Path(UPLOADS_DIR, 'avatars')
FILES_DIR = Path(UPLOADS_DIR, 'files')

BACKEND_CORS_ORIGINS = validate_backend_cors_origins()

if not UPLOADS_DIR.is_dir():
    UPLOADS_DIR.mkdir()
    
if not AVATARS_DIR.is_dir():
    AVATARS_DIR.mkdir()
    
if not FILES_DIR.is_dir():
    FILES_DIR.mkdir()
