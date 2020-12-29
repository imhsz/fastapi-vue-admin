from models.base import Base
from sqlalchemy import Column, BigInteger, DateTime, String
from datetime import datetime
from utils.snow_flake import generate_id


class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = ({"comment": "菜单表"})
    menu_id = Column(BigInteger, primary_key=True, index=True, default=generate_id, doc="菜单id")
    menu_name = Column(String(20), nullable=False, doc="菜单名称")
    menu_flag = Column(String(20), nullable=False, doc="前端标识")
    creat_time = Column(DateTime(), default=datetime.now, comment="创建时间")
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment="最后一次更新时间")

    def __repr__(self):
        return f"Menu:{self.menu_name}"



