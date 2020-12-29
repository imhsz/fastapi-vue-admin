from models.base import Base
from sqlalchemy import Column, String, DateTime, BigInteger
from datetime import datetime
from utils.snow_flake import generate_id


class Role(Base):
    __tablename__ = "role"
    __table_args__ = ({"comment": "角色表"})
    role_id = Column(BigInteger, primary_key=True, default=generate_id, index=True, doc="id")
    role_name = Column(String(20), nullable=False, doc="角色名称")
    role_desc = Column(String(100), doc="描述")
    creat_time = Column(DateTime(), default=datetime.now, comment="创建时间")
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment="最后一次更新时间")

    def __repr__(self):
        return f"Role:{self.role_name}"


class RoleUserRelation(Base):
    __tablename__ = "role_user"
    __table_args__ = ({"comment": "角色和用户关联表"})
    id = Column(BigInteger, primary_key=True, default=generate_id, index=True, doc="id")
    role_id = Column(BigInteger, doc="角色id")
    user_id = Column(BigInteger, doc="用户id")


class MenuRoleRelation(Base):
    __tablename__ = "role_menu"
    __table_args__ = ({"comment": "角色和菜单关联表"})
    id = Column(BigInteger, primary_key=True, default=generate_id, index=True, doc="id")
    role_id = Column(BigInteger, doc="角色id")
    menu_id = Column(BigInteger, doc="菜单id")


class PermRoleRelation(Base):
    __tablename__ = "role_perm"
    __table_args__ = ({"comment": "角色和权限关联表"})
    id = Column(BigInteger, primary_key=True, default=generate_id, index=True, doc="id")
    role_id = Column(BigInteger, doc="角色id")
    perm_id = Column(BigInteger, doc="权限id")
