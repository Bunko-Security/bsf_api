from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from fastapi import BackgroundTasks, HTTPException, UploadFile
from sqlalchemy import and_, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from service import get_user_by_login
from .schemas import BaseFileData
from schemas import UserAuthInfo
from .models import Files, FileUsers
from .utils import save_file_in_filesystem, delete_file_from_filesystem
from models import Users
from .exceptions import FileSavingException, NoDataForDecrypt, NoFileException


async def create_file(
    file_info: BaseFileData,
    file: UploadFile,
    user_from: str, 
    new_filename: str,
    db: AsyncSession
) -> int:
    new_file = Files(
        **file_info.model_dump(), 
        user_from=user_from, 
        filename=file.filename, 
        file_path=new_filename
    )
    db.add(new_file)
    try:
        await save_file_in_filesystem(file, new_filename)
        await db.commit()
        return new_file.file_id
    except FileSavingException:
        await db.rollback()
        raise FileSavingException


async def get_all_user_files(
    name_like: str,
    user_login: str,
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
                Files.user_from == user_login,
                or_(
                    FileUsers.user_to == user_login,
                    FileUsers.user_to.is_(None)
                )
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


async def get_fileinfo_by_file_id_and_user_login(
    file_id: int, 
    user_login: str, 
    db: AsyncSession
) -> Files:
    query = (
        select(Files).
        join(
            FileUsers, 
            and_(
                FileUsers.file_id == Files.file_id,
                or_(
                    FileUsers.user_to == user_login,
                    FileUsers.user_to.is_(None)
                )
            )
        ).
        where(Files.file_id == file_id)
    )
    
    result = (await db.scalars(query)).one_or_none()

    if result is None:
        raise NoFileException
    return result


async def delete_all_files_by_user_login(user_login: str, db: AsyncSession) -> None:
    query = (
        delete(Files).
        where(Files.user_from == user_login).
        returning(Files.file_path)
    )
    file_paths = (await db.execute(query)).all()
    if len(file_paths) == 0:
        return
    
    for filename in file_paths:
        delete_file_from_filesystem(filename[0])
    await db.commit()
        
        
async def delete_file_by_file_id_and_user_login(
    file_id: int, 
    user_login: str, 
    db: AsyncSession
) -> None:
    query = (
        delete(Files).
        where(
            and_(
                Files.user_from == user_login,
                Files.file_id == file_id
            )
        ).
        returning(Files.file_path)
    )
    filename = (await db.execute(query)).one_or_none()
    if filename is None:
        return
    delete_file_from_filesystem(filename[0])
    await db.commit()
    
    
async def get_all_files_to_user(
    name_like: str,
    user_login: str,
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
                FileUsers.user_to == user_login,
                Files.user_from != user_login
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


async def get_data_to_decrypt_private_file(
    file_id: int, 
    user_login: str, 
    db: AsyncSession
) -> FileUsers:
    query = (
        select(FileUsers).
        join(
            Files,
            and_(
                FileUsers.file_id == Files.file_id,
                or_(
                    FileUsers.user_to == user_login,
                    FileUsers.user_to.is_(None)
                    
                )
            )
        ).
        where(Files.file_id == file_id)
    )
    result = (await db.scalars(query)).one_or_none()
    if result is None:
        raise NoDataForDecrypt
    return result


async def read_fileuser_by_file_id(
    file_id: int,
    db: AsyncSession
) -> List[FileUsers]:
    query = (
        select(FileUsers).
        where(FileUsers.file_id == file_id)
    )
    return (await db.scalars(query)).all()
    