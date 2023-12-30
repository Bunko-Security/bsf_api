from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import BACKEND_CORS_ORIGINS
import src.auth.routers as auth
import src.profile.routers as profile
import src.files.routers as files
import src.coworkers.routers as coworkers
import src.users.routers as users


app = FastAPI(title='BSF API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(files.router)
app.include_router(coworkers.router)
app.include_router(users.router)
