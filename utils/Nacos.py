import requests


class Nacos:
    """
    Nacos api
    """
    def __init__(self, url, namespace):
        """
        :param url: Nacos的地址
        :param namespace: 应用的namespace
        """
        self.url = url
        self.namespace = namespace

    def get_config(self, data_id, group="DEFAULT_GROUP"):
        """
        获取配置项的值
        :param data_id: config的id
        :param group: 所属的group
        :return: 返回配置的值,如果此配置不存在就抛出ConfigNotFoundException
        """
        params = {"tenant": self.namespace, "dataId": data_id, "group": group}
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        config_request = requests.get(url=f"{self.url}/nacos/v1/cs/configs", params=params, headers=headers)
        config_value = config_request.text
        if config_value == "config data not exist\n":
            raise ConfigNotFoundException(data_id)
        return config_value


class ConfigNotFoundException(Exception):
    def __init__(self, config_name):
        self.config_name = config_name

    def __str__(self):
        return f"Error!!!Can't get {self.config_name} from Nacos Server,please check your dataId."
