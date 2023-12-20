from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import auth.routers
import profile.routers
import files.routers
import coworkers.routers
import users.routers


app = FastAPI(title='BSF API')

origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://localhost:3000', 'https://127.0.0.1:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(auth.routers.router)
app.include_router(profile.routers.router)
app.include_router(files.routers.router)
app.include_router(coworkers.routers.router)
app.include_router(users.routers.router)
