from typing import Annotated
from fastapi import APIRouter, Body, Depends, File, Path, Response, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.utils import get_current_user
from src.config import AVATARS_DIR
from src.schemas import UserAuthInfo

from .schemas import *
from .service import set_new_avatar, set_new_username, get_profile
from .validators import AvatarMimeTypeValidator, AvatarMaxSizeMBValidator, AvatarExtensionValidator
from pathlib import Path as ptPath
import hashlib

from PIL import Image


router = APIRouter(tags=['Profile'], prefix='/profile')


@router.put('/avatar', dependencies=[
    Depends(AvatarMimeTypeValidator), 
    Depends(AvatarMaxSizeMBValidator), 
    Depends(AvatarExtensionValidator)
    ])
async def set_avatar(
    new_avatar: UploadFile = File(...),
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> None:
    new_filename = hashlib.sha256(bytes(new_avatar.filename + current_user.login, encoding='utf-8')).hexdigest()
    new_filename += '.' + new_avatar.filename.split('.')[1]
    if current_user.avatar_path is not None:
        ptPath(AVATARS_DIR, current_user.avatar_path).unlink(missing_ok=True)
    path = ptPath(AVATARS_DIR, new_filename)
    im = Image.open(new_avatar.file)
    im.save(path)
    new = im.resize((400, 400))
    new.save(path)
    await set_new_avatar(current_user.login, new_filename, db)
    return Response(status_code=201)


# r'^[^\\/]{64}\.[^\\/]{3}$'
@router.get('/avatar/{filename}', status_code=204)
async def get_avatar(
    filename: Annotated[str, Path(pattern=r'^[a-z,0-9]{64}\.[a-z]{3}$')]
):
    path = ptPath(AVATARS_DIR, filename)
    if path.is_file():
        return FileResponse(path=path, status_code=200)
    else:
        return None


@router.get('')
async def get_profile_info(
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> PersonProfile:
    return await get_profile(current_user.login, db)

@router.put('/username')
async def set_username(
    new_username: Annotated[str, Body(embed=True)], 
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> None:
    await set_new_username(current_user.login, new_username, db)
    return Response(status_code=201)
