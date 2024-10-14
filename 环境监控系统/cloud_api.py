import requests
import json


class CloudApi:
    def __init__(self):
        self.resp_text = ''

    def resp_access_token(self, account, password):
        """
        响应获取AccessToken
        :param account:账号
        :param password:密码
        :return:
        """
        url = 'https://api.nlecloud.com/Users/Login'

        # post访问的包体
        data = {
            'Account': account,
            'Password': password,
            'IsRememberMe': True
        }

        # 使用request去请求网站
        resp_text = requests.post(url, data=data).content.decode('utf-8')
        self.resp_text = json.loads(resp_text)['ResultObj']['AccessToken']
        return resp_text

    def resp_get_device(self, devids):
        """
        获取设备数据
        :param devids: 设备ID
        :return: 设备列表清单
        """
        url = 'https://api.nlecloud.com/Devices/Datas'

        params = {
            'devIds': devids,
            'AccessToken': self.resp_text
        }
        resp = requests.get(url, params).content.decode('utf-8')
        resp = json.loads(resp)
        resp = resp['ResultObj'][0]['Datas']
        print(resp)
        return resp

    def resp_cmd_device(self, devids, apitag, data):
        """
        响应设备命令
        :param apitag:
        :param devids:
        :return:
        """
        url = 'https://api.nlecloud.com/Cmds'

        params = {
            'deviceId': devids,
            'apiTag': apitag,
            'AccessToken': self.resp_text
        }
        # 包体内容，用于控制设备，如打开1，关闭0，或者0-254调节
        json = data

        resp = requests.post(url, params=params, json=json).content.decode('utf-8')


if __name__ == '__main__':
    cloudapi = CloudApi()
    cloudapi.resp_access_token('19912345638', '123456')
    data = cloudapi.resp_get_device(1074613)
    cloudapi.resp_cmd_device(1074613, 'LED', '1')
