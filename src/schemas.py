from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str


class ResponseUser(BaseModel):
    id: int
    uuid_token: str

    class Config:
        orm_mode = True
