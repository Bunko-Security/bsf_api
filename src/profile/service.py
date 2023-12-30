from sqlalchemy.ext.asyncio import AsyncSession

from src.service import get_user_by_login

async def set_new_avatar(login: str, new_filename: str, db: AsyncSession):
    user = await get_user_by_login(login, db)
    user.avatar_path = new_filename
    await db.commit()

async def set_new_username(login: str, new_username: str, db: AsyncSession):
    user = await get_user_by_login(login, db)
    user.username = new_username
    await db.commit()
    
async def get_profile(login: str, db: AsyncSession):
    return await get_user_by_login(login, db)