from datetime import date
from fastapi import Form
from pydantic import BaseModel
from ..schemas import BaseFileData, SecretKey, FileInfo


class PrivateFileData(BaseFileData):
    @classmethod
    def as_form(cls,
                delete_date: date = Form(default=date.today()),
                ):
        return cls(delete_date=delete_date)
    
class EncryptPrivateFileData(SecretKey):
    user_to: str
    
