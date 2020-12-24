from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from core.db import get_session
from core.config import settings
from schema.user import Token
from models.user.models import User

login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SESSION_KEY = ""


def authenticate_user(username: str, password: str):
    """
    登陆认证
    """
    user = get_user(username)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


def create_access_token(*, data: dict):
    """
    生成JWT token
    """
    to_encode = data.copy()
    # 设置token过期时间
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY)
    return encoded_jwt


def get_user(username):
    """
    查询用户
    """
    db = get_session()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    获取当前登陆用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    校验用户是否被激活
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="用户未激活")
    # Todo 判断用户是否有权限访问接口
    return current_user


@login_router.post("/login", response_model=Token, name="用户登陆")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    获取token
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="帐号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="用户未激活!!!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return JSONResponse({"access_token": access_token.decode(), "token_type": "bearer"})


@login_router.post("/logout", name="用户登出")
def logout():
    return {"message": "已登出"}
