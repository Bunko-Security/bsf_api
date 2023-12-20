import json
from typing import Annotated, List, Optional
from fastapi import Body, Depends, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator, root_validator
from datetime import date
import json
    

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