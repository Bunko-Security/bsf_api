from typing import List, Optional
from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from src.database import get_async_session
from src.auth.utils import get_current_user
from src.schemas import UserAuthInfo
from src.config import FILES_DIR

from .schemas import FileInfo, DecryptPrivateFileData, FileToMeInfo
from .service import (
    delete_all_files_by_user_login, 
    get_all_user_files, 
    get_fileinfo_by_file_id_and_user_login,
    get_all_files_to_user,
    delete_file_by_file_id_and_user_login,
    get_data_to_decrypt_private_file
)
import src.files.private.routers as private
import src.files.public.routers as public

router = APIRouter(tags=['Files'], prefix='/files')
router.include_router(private.router)
router.include_router(public.router)

@router.delete('/my')
async def delete_all_my_files(
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> None:
    await delete_all_files_by_user_login(current_user.login, db)
    return Response(status_code=204)

@router.get('/my')
async def get_my_filenames(
    name_like: str = '',
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> List[FileInfo]:
    return await get_all_user_files(name_like, current_user.login, offset, limit, db)


@router.get('/to_me')
async def get_files_to_me(
    name_like: str = '',
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
)-> List[FileToMeInfo]:
    return await get_all_files_to_user(name_like, current_user.login, offset, limit, db)



@router.get('/{file_id}')
async def get_encrypt_file(
    file_id: int,
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    file_info = await get_fileinfo_by_file_id_and_user_login(file_id, current_user.login, db)
    return FileResponse(
        status_code=200, 
        filename=file_info.filename, 
        path=Path(FILES_DIR, file_info.file_path), 
        headers={"Access-Control-Expose-Headers": "Content-Disposition"}
    )


@router.delete('/{file_id}')
async def delete_my_file(
    file_id: int,
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> None:
    await delete_file_by_file_id_and_user_login(file_id, current_user.login, db)
    return Response(status_code=204)


@router.get('/{file_id}/data')
async def get_decrypt_file_data(
    file_id: int,
    current_user: UserAuthInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> DecryptPrivateFileData:
    fi = await get_data_to_decrypt_private_file(file_id, current_user.login, db)
    if fi.user_to is None:
        return DecryptPrivateFileData(
            secret_key=fi.secret_key,
            priv_key=None
        )
    return DecryptPrivateFileData(
            secret_key=fi.secret_key,
            priv_key=current_user.priv_key
        )
