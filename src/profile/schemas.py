from pydantic import BaseModel, ConfigDict, validator

class PersonProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    login: str
    username: str
    avatar_path: str | None
    is_admin: bool
    
    @validator('avatar_path')
    def validate_avatar_path(cls, value):
        if value is None:
            return value
        else:
            return 'http://localhost:8000/profile/avatar/' + value # Прямой путь ???