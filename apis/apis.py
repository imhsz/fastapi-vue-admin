from fastapi import APIRouter, Depends
from apis.login.controller import get_current_active_user
from apis.login.controller import login_router
from apis.users.controller import user_router
from apis.record.controller import record_router
from apis.role.controller import role_router

api_router = APIRouter()
# router注册
api_router.include_router(login_router, tags=["login"])
api_router.include_router(user_router, prefix="/users", tags=["users"], dependencies=[Depends(get_current_active_user)])
api_router.include_router(record_router, prefix="/record", tags=["record"],
                          dependencies=[Depends(get_current_active_user)])
api_router.include_router(role_router, prefix="/role", tags=["role"], dependencies=[Depends(get_current_active_user)])
