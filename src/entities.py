from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    verified: bool = False
    first_name: str
    last_name: str
    picture: str
    sso_id: str

class UserUpdate(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False
    
    
class FollowerOperation(BaseModel):
    user_id: str
    follower_user_id: str