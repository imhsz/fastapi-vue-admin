from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserBase(BaseModel):
    """
    User schema基础格式
    """
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    nick_name: str
    avatar: str = "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
    menus: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "username": "huangtao",
                "email": "huangtao123689@gmail.com",
                "is_active": True,
                "nick_name": "huangtao",
                "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
            }
        }


class NewUser(UserBase):
    """
    新建用户schema
    """
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "huangtao",
                "email": "huangtao123689@gmail.com",
                "is_active": True,
                "nick_name": "huangtao",
                "password": "123456"
            }
        }


class AllUser(BaseModel):
    """
    所有用户schema
    """
    total: int
    users: List[UserBase] = []

    class Config:
        schema_extra = {
            "example": {"total": 50, "users": [
                {"username": "huangtao", "email": "huangtao123689@gmail.com", "is_active": True, "nick_name": "mark"},
                {"username": "huangtao1", "email": "huangtao1@gmail.com", "is_active": True, "nick_name": "huangtao1"}]
                        }
        }


class ModifyUser(BaseModel):
    """
    修改用户schema
    """
    username: Optional[str] = None
    password: Optional[str] = None
    email: EmailStr
    is_active: Optional[bool] = True
    nick_name: str


class Token(BaseModel):
    """
    token schema
    """
    access_token: str
    token_type: str
