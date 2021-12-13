from typing import List, Optional

from pydantic import BaseModel

class Login(BaseModel):
    email   : str = 'test9@gmail.com'
    password: str = '!test999'

class Signup(BaseModel):
    email   : str = 'test9@gmail.com'
    name    : str = 'test'
    password: str = '!test999'

class User(BaseModel):
    id       : int
    email    : str
    name     : str
    password : str
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    Token: str
    