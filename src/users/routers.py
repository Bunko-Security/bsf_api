from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from src.auth.utils import get_current_user
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserAuthInfo
from src.auth.utils import get_current_user_admin
from .service import read_all_users, delete_user, create_user, read_users_by_logins
from .schemas import UserInfo, UserCreate, UserPubkey
from .exceptions import UserAlreadyExists


router = APIRouter(tags=['Users'], prefix='/users')


@router.get('', dependencies=[Depends(get_current_user_admin)])
async def get_all_users(
    name_like: str = '',
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> List[UserInfo]:
    return await read_all_users(name_like, offset, limit, current_user.login, db)


@router.post('', dependencies=[Depends(get_current_user_admin)], status_code=201)
async def register_user(
    user: UserCreate, 
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> None:
    try:
        await create_user(user, db)
    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail='Этот пользователь уже создан')
    
@router.delete('/{login}', dependencies=[Depends(get_current_user_admin)], status_code=204)
async def remove_user(
    login: str, 
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> None:
    if login == current_user.login:
        raise HTTPException(status_code=409, detail='Нельзя удалить себя')
    await delete_user(login, db)


@router.post('/pub_keys')
async def get_user_pubkeys_to_encrypt(
    logins: List[str],
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> List[UserPubkey]:
    user_pubkeys: List[UserPubkey] = await read_users_by_logins(logins, db)
    user_pubkeys.append(UserPubkey(
        login=current_user.login, pub_key=current_user.pub_key
    ))
    return user_pubkeys