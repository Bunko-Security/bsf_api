from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models import Users


async def get_user_by_login(
    login: str, db: AsyncSession
) -> Optional[Users]:
    return await db.get(Users, login)
