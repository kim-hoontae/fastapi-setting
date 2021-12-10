from typing import List, Optional

from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name : str
    password: str

class User(BaseModel):
    id       : int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    Authorization: str = None