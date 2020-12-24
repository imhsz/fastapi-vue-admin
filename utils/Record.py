import json
from core.db import get_session
from models.record.models import OperateRecords


class Record:
    @staticmethod
    def create_operate_record(username, ip, old_object=None, new_object=None):
        """
        创建修改记录
        @param old_object: 修改前的类
        @param new_object: 修改后的类
        @param username: 修改用户名
        @param ip: 修改ip
        @return:
        """
        # 获取修改的类名
        operate_object = new_object.__class__.__name__ if new_object else old_object.__class__.__name__
        # 判断修改的类型
        if not old_object:
            operate_type = "新增"
            operate_detail = new_object.__dict__
            operate_detail.pop("_sa_instance_state")
            # ensure_ascii设为False,这样存入数据库不会变成unicode码
            operate_detail = json.dumps(operate_detail, ensure_ascii=False)
        elif not new_object:
            operate_type = "删除"
            operate_detail = old_object.__dict__
            operate_detail.pop("_sa_instance_state")
            operate_detail = json.dumps(operate_detail, ensure_ascii=False)
        else:
            operate_type = "修改"
            # __dict__获取所有类所有属性
            old_object_dict = old_object.__dict__
            old_object_dict.pop("_sa_instance_state")
            new_object_dict = new_object.__dict__
            new_object_dict.pop("_sa_instance_state")
            operate_detail = []
            for field in old_object_dict.keys():
                if old_object_dict[field] != new_object_dict[field]:
                    operate_detail.append({"name": field, "old": old_object_dict[field], "new": new_object_dict[field]})
            if len(operate_detail) == 0:
                # 说明没有修改,不必记录
                return
            operate_detail = json.dumps(operate_detail, ensure_ascii=False)

        record_dict = {"operate_object": operate_object, "operate_type": operate_type, "operate_detail": operate_detail,
                       "operate_ip": ip, "operate_username": username}
        db = get_session()
        operate_record = OperateRecords(**record_dict)
        db.add(operate_record)
        db.commit()
