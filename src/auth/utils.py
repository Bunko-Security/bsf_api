from enum import Enum
from typing import Annotated, Dict
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import UserAuthInfo
from src.database import get_async_session
from src.service import get_user_by_login

from .config import SECRET_KEY, ACCESS_TOKEN_ALIVE, REFRESH_TOKEN_ALIVE
from .schemas import Tokens

class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


def create_token(
    user_login: str, token_type: TokenType
) -> str:
    to_encode = {'login': user_login}
    if token_type == TokenType.ACCESS:
        to_encode.update({
		'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_ALIVE),
		'sub': token_type.value
	})
    elif token_type == TokenType.REFRESH:
        to_encode.update({
		'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_ALIVE),
		'sub': token_type.value
	})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt


def decode_token(
    token: str, token_type: TokenType
) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    if payload.get('sub') != token_type.value:
        raise JWTError
    login: str = payload.get("login")
    if login is None:
        raise JWTError
    return login


def get_all_tokens(login: str) -> Tokens:
    return Tokens(
        access_token=create_token(login, TokenType.ACCESS),
        refresh_token=create_token(login, TokenType.REFRESH)
    )


oauth2_scheme = HTTPBearer()
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session)
) -> UserAuthInfo:
    try:
        login = decode_token(credentials.credentials, TokenType.ACCESS)
        user = await get_user_by_login(login, db)
        if user is None:
            raise JWTError
        return UserAuthInfo.model_validate(user)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail='Token expired! Please refresh it!'
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )


RefreshSession: Dict[str, str] = {}
async def get_current_user_by_refresh(
    res: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    db: AsyncSession = Depends(get_async_session)
) -> UserAuthInfo:
    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="No refresh token",
        )
    
    res.delete_cookie('refresh_token')
    headers = {'set-cookie': res.headers.get('set-cookie')}

    try:
        login = decode_token(refresh_token, TokenType.REFRESH)
        user = await get_user_by_login(login, db)
        if user is None or refresh_token != RefreshSession.get(user.login):
            raise JWTError
        return UserAuthInfo.model_validate(user)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail='Token expired! Please login in your account again!',
            headers=headers
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers=headers
        )
  
        
def get_current_user_admin(current_user: Annotated[UserAuthInfo, Depends(get_current_user)]):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
