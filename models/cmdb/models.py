from models.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from utils.snow_flake import generate_id
from datetime import datetime


class CMDBType(Base):
    __tablename__ = "cmdb_type"
    __table_args__ = ({"comment": "CMDB类型表"})
    cmdb_type_id = Column(BigInteger, primary_key=True, index=True, default=generate_id, doc="cmdb类型id")
    cmdb_type_name = Column(String(100), nullable=False)
    cmdb_type_parent_id = Column(BigInteger)

    def __repr__(self):
        return f"CMDBType:{self}"


class CMDBDesc(Base):
    __tablename__ = "cmdb_desc"
    __table_args__ = ({"comment": "CMDB具体属性表"})
    cmdb_desc_id = Column(BigInteger, primary_key=True, index=True, default=generate_id, doc="cmdb属性id")


class CMDBRecord(Base):
    __tablename__ = "cmdb_record"
    __table_args__ = ({"comment": "CMDB数据记录表"})
    cmdb_record_id = Column(BigInteger, primary_key=True, index=True, default=generate_id, doc="cmdb记录id")
