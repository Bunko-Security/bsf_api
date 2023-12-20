from datetime import date

from fastapi import Form
from ..schemas import BaseFileData, FileToMeInfo, SecretKey


class PublicFileData(BaseFileData, SecretKey):
    @classmethod
    def as_form(cls,
                delete_date: date = Form(...),
                secret_key: str = Form(...)
    ):
        return cls(delete_date=delete_date, secret_key=secret_key)

class PublicFileInfo(FileToMeInfo):
    pass