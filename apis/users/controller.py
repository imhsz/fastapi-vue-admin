from copy import deepcopy
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from core.db import get_db
from models.user.models import User
from sqlalchemy.orm import Session
from schema.user import UserBase, NewUser, AllUser, ModifyUser
import jwt
from core.config import settings
from utils.Record import Record

user_router = APIRouter()


@user_router.get("/me", response_model=UserBase, name="获取登陆用户详情")
def me(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    # 通过Header中的token获取已经登陆的用户名
    payload = jwt.decode(authorization.split(" ")[-1], settings.SECRET_KEY)
    username: str = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    user_dict = {"username": user.username, "email": user.email, "is_active": user.is_active,
                 "nick_name": user.nick_name, "menus": ["system-manage", "user-manage", "record-manage", "user-add"]}
    return UserBase(**user_dict)


@user_router.get("/get_user_info", response_model=UserBase, name="获取指定用户详情")
def get_user_info(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user_dict = {"username": user.username, "email": user.email, "is_active": user.is_active,
                     "nick_name": user.nick_name}
        return UserBase(**user_dict)
    else:
        raise HTTPException(status_code=406, detail="用户不存在")


@user_router.get("/all_users", response_model=AllUser, name="获取所有用户")
def all_users(page_no: int, page_size: int, search_username: str = '', db: Session = Depends(get_db)):
    # 分页查询,前端需要传递页数,和每页多少个
    # 数据分页与list切片格式保持一致
    if search_username:
        total = db.query(User).filter(User.username == search_username).count()
        users = db.query(User).filter(User.username == search_username).slice(page_size * (page_no - 1),
                                                                              page_size * page_no)
    else:
        total = db.query(User).count()
        users = db.query(User).slice(page_size * (page_no - 1), page_size * page_no)
    all_users_dict = {"total": total, "users": [UserBase(
        **{"username": user.username, "email": user.email, "is_active": user.is_active, "nick_name": user.nick_name})
        for user in users]}
    return AllUser(**all_users_dict)


@user_router.put("/create_user", responses={406: {"description": "创建的用户已经存在"}}, name="创建新用户")
def create_user(user: NewUser, request: Request, operator: Optional[str] = Header(None), db: Session = Depends(get_db)):
    old_user = db.query(User).filter(User.username == user.username).first()
    old_email = db.query(User).filter(User.email == user.email).first()
    if old_user or old_email:
        raise HTTPException(status_code=406, detail="创建的用户已经存在")
    user_dict = {"username": user.username, "email": user.email, "nick_name": user.nick_name,
                 "is_active": user.is_active}
    new_user = User(**user_dict)
    new_record = deepcopy(new_user)
    new_user.convert_pass_to_hash(user.password)
    db.add(new_user)
    db.commit()
    # 调用数据修改记录器
    Record.create_operate_record(new_object=new_record, username=operator, ip=request.client.host)
    return {"message": "用户创建成功"}


@user_router.post("/update_user", name="更新用户信息")
def update_user(request: Request, modify_user: ModifyUser, operator: Optional[str] = Header(None),
                db: Session = Depends(get_db)):
    """
    用户名不可以修改
    """
    user = db.query(User).filter(User.username == modify_user.username).first()
    if user:
        old_user = deepcopy(user)
        if modify_user.password:
            user.convert_pass_to_hash(modify_user.password)
        user.is_active = modify_user.is_active
        user.email = modify_user.email
        user.nick_name = modify_user.nick_name
        new_user = deepcopy(user)
        db.add(user)
        db.commit()
        # 调用数据修改记录器
        Record.create_operate_record(old_object=old_user, new_object=new_user, username=operator,
                                     ip=request.client.host)
        return {"message": "用户信息更新成功"}
    else:
        raise HTTPException(status_code=406, detail="用户不存在")
