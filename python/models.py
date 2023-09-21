from pydantic import BaseModel

class Account(BaseModel):
    uid: str
    email: str
    name: str


class Role(BaseModel):
    rid: str


class Permission(BaseModel):
    pid: str