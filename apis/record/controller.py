from fastapi import APIRouter, Depends
from core.db import get_db
from sqlalchemy.orm import Session
from models.record.models import OperateRecords
from schema.record import Record, AllRecords

record_router = APIRouter()


@record_router.get("/all_records", response_model=AllRecords, name="获取所有数据操作记录")
def all_records(page_no: int, page_size: int, search_info: str, db: Session = Depends(get_db)):
    if search_info:
        total = db.query(OperateRecords).filter(OperateRecords.operate_detail.like(f"%{search_info}%")).count()
        records = db.query(OperateRecords).filter(OperateRecords.operate_detail.like(f"%{search_info}%")).order_by(
            OperateRecords.operate_time.desc()).slice(page_size * (page_no - 1),
                                                      page_size * page_no)
    else:
        total = db.query(OperateRecords).count()
        records = db.query(OperateRecords).order_by(OperateRecords.operate_time.desc()).slice(page_size * (page_no - 1),
                                                                                              page_size * page_no)
    record_lists = {"total": total, "records": [Record(
        **{"operate_object": record.operate_object, "operate_type": record.operate_type,
           "operate_detail": record.operate_detail,
           "operate_ip": record.operate_ip, "operate_username": record.operate_username,
           "operate_time": record.operate_time}) for record in records]}
    return AllRecords(**record_lists)
