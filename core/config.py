from pydantic import AnyHttpUrl
from typing import List
import os

ENV = os.environ.get("fast_env", "DEV")  # 本次启动环境


class Settings:
    APP_NAME = "fastapi-vue-admin"
    # api前缀
    API_PREFIX = "/api"
    # jwt密钥,建议随机生成一个
    SECRET_KEY = "ShsUP9qIP2Xui2GpXRY6y74v2JSVS0Q2YOXJ22VjwkI"
    # token过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60
    # 跨域白名单
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:9528"]
    # db配置
    DB_URL = "mysql+pymysql://root:Aa123456@127.0.0.1:3306/fast"
    # 启动端口配置
    PORT = 8999
    # 是否热加载
    RELOAD = True


settings = Settings()
