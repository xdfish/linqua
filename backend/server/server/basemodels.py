from pydantic import BaseModel
from typing import *

#User Basemodel Spezifikation
class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    role: Literal['ADMIN', 'USER']

#User Information Spezifikation
class UserInfo(UserBase):
    created: str
