from typing import List, Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import FileUsers, Files

async def create_public_fileuser(
    secret_key: str, 
    file_id: int, 
    db: AsyncSession
) -> None:
    new_file_users = FileUsers(
        file_id=file_id, user_to=None, secret_key=secret_key
    )
    db.add(new_file_users)
    await db.commit()
    

async def get_all_public_files(
    name_like: str, 
    offset: Optional[int],
    limit: Optional[int], 
    db: AsyncSession
) -> List[Files]:
    query = (
        select(Files).
        join(
            FileUsers, 
            and_(
                FileUsers.file_id == Files.file_id,
                FileUsers.user_to.is_(None)
            )
        ).
        where(
            Files.filename.contains(name_like)
        ).
        order_by(Files.file_id).
        offset(offset).
        limit(limit)
    )
    return (await db.scalars(query)).all()
