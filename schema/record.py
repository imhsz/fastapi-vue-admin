from pydantic import BaseModel
from typing import List
from datetime import datetime


class Record(BaseModel):
    """
    单条记录schema
    """
    operate_object: str
    operate_type: str
    operate_detail: str
    operate_ip: str
    operate_username: str
    operate_time: datetime


class AllRecords(BaseModel):
    """
    所有操作记录schema
    """
    total: int
    records: List[Record]

    class Config:
        schema_extra = {
            "example": {"total": 50, "records": [
                {"operate_object": "User", "operate_type": "修改",
                 "operate_detail": '[{"name": "nick_name", "old": "admin1", "new": "admin"}]',
                 "operate_ip": "127.0.0.1", "operate_username": "admin"}]
                        }
        }
