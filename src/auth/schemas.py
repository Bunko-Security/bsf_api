from pydantic import BaseModel

class UserBase(BaseModel):
    login: str

class UserLogin(UserBase):
    auth_hash: str

class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    
class HashKey(BaseModel):
    hash_key: str