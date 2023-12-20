import base64
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from schemas import UserAuthInfo

from .utils import (
    get_all_tokens, 
    get_async_session, 
    get_current_user, 
    get_current_user_by_refresh, 
    RefreshSession
)
from .hash import verify_auth_key
from service import get_user_by_login
from .schemas import UserLogin, HashKey
from .exceptions import  InvalidUserLogin, InvalidUserPassword

router = APIRouter(tags=['Authentication'], prefix='/auth')

@router.get('/hash_key')
async def get_hash_key(
    login: str, db: AsyncSession = Depends(get_async_session)
) -> HashKey:
    user = await get_user_by_login(login, db)
    if user is None:
        fake_key = base64.b64encode(
            hashlib.sha256(login.encode()).digest()[:22]
        ).decode()
        return HashKey(
            hash_key=fake_key
        )
    else:
        return HashKey(
            hash_key=user.hash_key
        )


@router.post('/login')
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(get_async_session)
) -> None:
    try:
        user = await get_user_by_login(login_data.login, db)
        if user is None:
            raise InvalidUserLogin
        if not verify_auth_key(login_data.login, login_data.auth_hash, user.auth_hash):
            raise InvalidUserPassword
        tokens = get_all_tokens(user.login)
        response = Response()
        RefreshSession[user.login] = tokens.refresh_token
        response.set_cookie('access_token', value=tokens.access_token)
        response.set_cookie('refresh_token', value=tokens.refresh_token, httponly=True)
        return response
    except (InvalidUserLogin, InvalidUserPassword):
        raise HTTPException(status_code=404, detail='Не верные данные')


@router.get('/refresh')
async def refresh(
    current_user: UserAuthInfo = Depends(get_current_user_by_refresh)
) -> None:
    tokens = get_all_tokens(current_user.login)
    response = Response()
    RefreshSession[current_user.login] = tokens.refresh_token
    response.set_cookie('access_token', value=tokens.access_token)
    response.set_cookie('refresh_token', value=tokens.refresh_token, httponly=True)
    return response

@router.get('/logout')
async def logout(
    current_user: UserAuthInfo = Depends(get_current_user)
) -> None:
    response = Response()
    try:
        del RefreshSession[current_user.login]
    except KeyError:
        pass
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token', httponly=True)
    return response