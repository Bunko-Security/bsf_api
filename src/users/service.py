from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.hash import bcrypt_auth_key
from src.models import Users
from sqlalchemy import and_, delete, select

from .exceptions import UserAlreadyExists
from .schemas import UserCreate
from .utils import delete_avatar_from_filesystem

async def read_all_users(
    name_like: str, 
    offset: Optional[int],
    limit: Optional[int], 
    user_login: str,
    db: AsyncSession
) -> List[Users]:
    query = (
        select(Users).
        where(
            and_(
                Users.login != user_login,
                Users.login.contains(name_like)
            )
        ).
        order_by(Users.login).
        offset(offset).
        limit(limit)
    )
    return (await db.scalars(query)).all()


async def create_user(
    user: UserCreate, db: AsyncSession
) -> None:
    if await db.get(Users, user.login):
        raise UserAlreadyExists
    user.auth_hash = bcrypt_auth_key(user.login, user.auth_hash)
    new_user = Users(**user.model_dump())
    db.add(new_user)
    await db.commit()
    
async def delete_user(user_login: str, db: AsyncSession):
    query = (
        delete(Users).
        where(Users.login == user_login).
        returning(Users)
    )
    delete_user = (await db.scalars(query)).one_or_none()
    if delete_user is None:
        return
    if delete_user.avatar_path is not None:
        delete_avatar_from_filesystem(delete_user.avatar_path)
    await db.commit()
    
    
async def read_users_by_logins(
    user_logins: List[str], 
    db: AsyncSession
) -> List[Users]:
    query = (
        select(Users).
        where(Users.login.in_(user_logins))
    )
    return (await db.scalars(query)).all()