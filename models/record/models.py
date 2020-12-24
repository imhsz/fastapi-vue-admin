from models.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime
from datetime import datetime
from utils.snow_flake import generate_id


class OperateRecords(Base):
    __tablename__ = "operate_records"
    __table_args__ = ({"comment": "数据操作记录表"})
    record_id = Column(BigInteger(), default=generate_id, index=True, primary_key=True)
    operate_username = Column(String(20), nullable=False, index=True, comment="操作的用户")
    operate_time = Column(DateTime(), default=datetime.now, comment="操作的时间")
    operate_ip = Column(String(20), nullable=False, comment="操作的IP")
    operate_type = Column(String(10), nullable=False, comment="操作类型")
    operate_object = Column(String(30), nullable=False, comment="操作的对象")
    operate_detail = Column(String(200), comment="操作的具体信息")
