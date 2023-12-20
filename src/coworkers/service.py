from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import and_, delete, or_, select, union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from models import Users
from .models import Coworkers

from .schemas import CoworkerBase
from pydantic import TypeAdapter
from .exceptions import CoworkerAlreadyExists, InvalidCoworkerLogin


async def all_coworkers_by_user_login(
    user_login: str,
    login_like: str,
    offset: Optional[int], 
    limit: Optional[int], 
    db: AsyncSession
) -> List[Users]:
    query = (
        select(Users).
        join(
            Coworkers,
            and_(
                Coworkers.user_to == Users.login,
                Coworkers.user_from == user_login
            )
        ).
        where(Users.login.contains(login_like)).
        order_by(Users.login).
        offset(offset).
        limit(limit)
    )
    return (await db.scalars(query)).all()


async def all_no_coworkers_by_user_login(
    user_login: str,
    login_like: str,
    offset: Optional[int], 
    limit: Optional[int], 
    db: AsyncSession
) -> List[Users]:
    query = (
        select(Users).
        outerjoin(
            Coworkers,
            and_(
                Coworkers.user_to == Users.login,
                Coworkers.user_from == user_login
            )
        ).
        where(
            and_(
                Coworkers.user_from.is_(None),
                Users.login != user_login,
                Users.login.contains(login_like)
            )
        ).
        order_by(Users.login).
        offset(offset).
        limit(limit)
    )
    return (await db.scalars(query)).all()

async def create_coworker(
    user_login: str,
    friend_login: str,
    db: AsyncSession
) -> None:
    if await db.get(Coworkers, (user_login, friend_login)):
        raise CoworkerAlreadyExists
    try:
        new_friend = Coworkers(
            user_from=user_login,
            user_to=friend_login
        )
        db.add(new_friend)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise InvalidCoworkerLogin

async def delete_coworker(
    user_login: str,
    friend_login: str,
    db: AsyncSession
) -> None:
    query = (
        delete(Coworkers).
        where(
            and_(
                Coworkers.user_from == user_login,
                Coworkers.user_to == friend_login
            )
        )
    )
    await db.execute(query)
    await db.commit()
