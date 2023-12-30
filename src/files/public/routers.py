import datetime
import hashlib
from typing import List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_current_user
from src.database import get_async_session
from src.schemas import UserAuthInfo

from ..exceptions import FileSavingException
from ..schemas import BaseFileData
from ..service import create_file

from .schemas import PublicFileData, PublicFileInfo
from .service import create_public_fileuser, get_all_public_files

router = APIRouter(prefix='/public')


@router.post('', status_code=201)
async def upload_public_file(
    file_info: PublicFileData = Depends(PublicFileData.as_form),
    file: UploadFile = File(),
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> None:
    salt = current_user.login \
        + datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S') \
        + file_info.delete_date.isoformat()
    new_filename = hashlib.sha256(
        bytes(file.filename + salt, encoding='utf-8')
    ).hexdigest()
    try:
        file_id: int = await create_file(
            BaseFileData(delete_date=file_info.delete_date), file, current_user.login, new_filename, db
        )
        await create_public_fileuser(file_info.secret_key, file_id, db)
    except FileSavingException:
        await db.rollback()
        raise HTTPException(status_code=503, detail='File could not be saved')
    
@router.get('')
async def get_public_files(
    name_like: str = '',
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> List[PublicFileInfo]:
    return await get_all_public_files(name_like, offset, limit, db)
