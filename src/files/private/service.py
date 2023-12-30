from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Users

from ..service import read_fileuser_by_file_id
from ..exceptions import FileUsersAlreadyExists
from ..models import FileUsers

from .schemas import EncryptPrivateFileData

async def create_private_fileuser(
    file_users_info: List[EncryptPrivateFileData], 
    file_id: int, 
    db: AsyncSession
) -> None:
    if len(await read_fileuser_by_file_id(file_id, db)) != 0:
        raise FileUsersAlreadyExists
    for fu in file_users_info:
        if await db.get(Users, fu.user_to):
            new_file_users = FileUsers(**fu.model_dump(), file_id=file_id)
            db.add(new_file_users)
    await db.commit()
