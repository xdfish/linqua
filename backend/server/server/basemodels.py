from pydantic import BaseModel
from typing import *

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    role: Literal['ADMIN', 'USER']

class UserInfo(UserBase):
    created: str
