import imghdr
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Type, cast
from fastapi import Depends, HTTPException, UploadFile


class AvatarMimeTypeValidator:
    def __init__(self) -> None:
        pass
    
    def __call__(self, new_avatar: UploadFile):
        if new_avatar.content_type not in ['image/jpeg', 'image/png']:
            raise HTTPException(400, detail='Invalid document type')
        return new_avatar


class AvatarMaxSizeMBValidator:
    def __init__(self) -> None:
        pass

    def __call__(self, new_avatar: UploadFile):
        if new_avatar.size > 5 * 1024 * 1024:
            raise HTTPException(400, detail='File size more than 5 MB')
        return new_avatar


class AvatarExtensionValidator:
    def __init__(self) -> None:
        pass

    def __call__(self, new_avatar: UploadFile):
        if imghdr.what(new_avatar.file) not in ['jpeg', 'png']:
            raise HTTPException(400, detail='Invalid document type')
        return new_avatar


# def avatar_check_mime_type(new_avatar: UploadFile):
#     if new_avatar.content_type not in ['image/jpeg', 'image/png']:
#         raise HTTPException(400, detail='Invalid document type')
#     return new_avatar

# def avatar_check_max_size(new_avatar: UploadFile):
#     if new_avatar.size > 5 * 1024 * 1024:
#         raise HTTPException(400, detail='File size more than 5 MB')
#     return new_avatar

# def avatar_check_file_type(new_avatar: UploadFile):
#     if imghdr.what(new_avatar.file) not in ['jpeg', 'png']:
#         raise HTTPException(400, detail='Invalid document type')
#     return new_avatar