from typing import Optional
from pydantic import BaseModel
from datetime import date
    

class SecretKey(BaseModel):
    secret_key: str

class FileID(BaseModel):
    file_id: int


class BaseFileData(BaseModel):
    delete_date: date

class FileInfo(FileID, BaseFileData):
    filename: str

class FileToMeInfo(FileInfo):
    user_from: str

class DecryptPrivateFileData(SecretKey):
    priv_key: Optional[str]