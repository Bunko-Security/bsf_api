from pydantic import BaseModel, ConfigDict


class UserAuthInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    login: str
    avatar_path: str | None
    pub_key: str
    priv_key: str
    is_admin: bool