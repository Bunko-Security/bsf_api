from typing import Annotated, List, Optional
from fastapi import APIRouter, Body, Depends, File, Response, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.utils import get_current_user
from config import AVATARS_DIR
from schemas import UserAuthInfo
from .schemas import CoworkerBase, CoworkerLogin
from .service import *
from .exceptions import CoworkerAlreadyExists, InvalidCoworkerLogin
router = APIRouter(tags=['Coworkers'], prefix='/coworkers')

@router.get('/favorite')
async def get_all_favorite_coworkers(
    name_like: str = '',
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> List[CoworkerBase]:
    return await all_coworkers_by_user_login(current_user.login, name_like, offset, limit, db)

@router.get('/other')
async def get_all_no_favorite_coworkers(
    name_like: str = '',
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> List[CoworkerBase]:
    return await all_no_coworkers_by_user_login(current_user.login, name_like, offset, limit, db)

@router.post('/favorite')
async def add_new_favorite_coworker(
    coworker_login: CoworkerLogin,
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> None:
    try:
        await create_coworker(current_user.login, coworker_login.login, db)
        return Response(status_code=201)
    except CoworkerAlreadyExists:
        raise HTTPException(status_code=409, detail='Friend already exists')
    except InvalidCoworkerLogin:
        raise HTTPException(status_code=404, detail='Invalid friend login')

    
@router.delete('/{coworker_login}')
async def delete_coworker_from_favorite(
    coworker_login: str,
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> None:
    await delete_coworker(current_user.login, coworker_login, db)
    return Response(status_code=204)