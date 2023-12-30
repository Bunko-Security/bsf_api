import datetime
import hashlib

from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_current_user
from src.database import get_async_session
from src.schemas import UserAuthInfo

from ..schemas import FileID
from ..service import create_file
from ..exceptions import FileSavingException, FileUsersAlreadyExists

from .schemas import EncryptPrivateFileData, PrivateFileData
from .service import create_private_fileuser

router = APIRouter(prefix='/private')

@router.post('', status_code=201)
async def upload_private_file(
    file_info: PrivateFileData = Depends(PrivateFileData.as_form),
    file: UploadFile = File(),
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> FileID:
    salt = current_user.login \
        + datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S') \
        + file_info.delete_date.isoformat()
    new_filename = hashlib.sha256(
        bytes(file.filename + salt, encoding='utf-8')
    ).hexdigest()
    try:
        file_id: int = await create_file(
            file_info, file, current_user.login, new_filename, db
        )
        return FileID(file_id=file_id)
    except FileSavingException:
        raise HTTPException(status_code=503, detail='File could not be saved')
    

@router.post('/{file_id}/data', status_code=201)
async def create_private_file_data(
    file_id: int, 
    file_data: List[EncryptPrivateFileData], 
    current_user: UserAuthInfo = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
) -> None:
    try:
        await create_private_fileuser(file_data, file_id, db)
    except FileUsersAlreadyExists:
        raise HTTPException(status_code=409, detail='File Info Already Exists')