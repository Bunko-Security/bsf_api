from pydantic import BaseModel, ConfigDict

class CoworkerLogin(BaseModel):
    login: str

class CoworkerBase(CoworkerLogin):
    model_config = ConfigDict(from_attributes=True)

    username: str
