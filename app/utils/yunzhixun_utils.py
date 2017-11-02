# -*- coding: UTF-8 -*-
import hashlib
import datetime
import base64
import json
import requests
import random
from config import Config


class YzxAPI:

    baseUrl = Config.YZX_URL
    version = Config.YZX_VERSION
    accountSid = Config.YZX_ACCOUNTSID
    token = Config.YZX_TOKEN
    appId = Config.YZX_APPID

    @staticmethod
    def get_timestamp():
        """
        获取时间戳
        """
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def get_message_code():
        return random.randint(1000, 9999)

    def get_sig_param(self, timestamp):
        """
        获取签名参数
        :param timestamp: 时间戳
        """
        sig = self.accountSid + self.token + timestamp
        return hashlib.md5(bytes(sig, encoding='utf-8')).hexdigest().upper()

    def get_auth_info(self, timestamp):
        """
        获取授权信息

        :param timestamp: 时间戳
        """
        sig = self.accountSid + ':' + timestamp.strip()
        return base64.b64encode(sig.encode())

    def get_url(self, service, service_param, timestamp):
        """
        获取url
        :param service: 业务类型
        :param service_param: 业务参数
        :param timestamp: 时间戳
        """
        fmt = self.baseUrl
        url = fmt.format(self.version, self.accountSid, service, service_param, self.get_sig_param(timestamp))
        print(url)
        return url

    def send_http_request(self, service, service_param, body=None):
        """
        发送HTTP请求
        :param service: 业务类型
        :param service_param: 业务参数
        :param body: 请求包体
        """
        timestamp = self.get_timestamp()
        url = self.get_url(service, service_param, timestamp)
        try:
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json;charset=utf-8',
                       'Authorization': self.get_auth_info(timestamp)}
            data = {}

            if body:
                headers['Content-Length'] = str(len(body))
                print(body)
                data = body
                print(headers)

            r = requests.post(url, data=data, headers=headers, timeout=10)
            response = r.json()
        except requests.HTTPError as e:
            print(e.errno)
            response = None
        return response

    def tw_bn_alloc(self, caller, callee, city_id):
        """
        双向绑定号码申请接口

        :param caller: 主叫号码
        :param callee: 被叫号码
        :param city_id: 城市ID 格式为 0086+去零区号
        """
        body = {
            # "hangupUrl": "",
            "caller": caller,
            "appId": self.appId,
            "callerRingName": "a.mp3",
            # "requestId": "111111",
            "calleeDisplayNum": "02188888",
            "maxAge": "300",
            # "record": "0",
            "maxAllowTime": "10",
            # "dstVirtualNum": "02188888",
            "calleeRingName": "b.mp3",
            # "statusUrl": "",
            "callee": callee,
            # "recordUrl": "",
            "cityId": city_id
        }
        return self.send_http_request('safetyCalls', 'allocNumber', json.dumps(body))

    def tw_bn_free(self, bind_id, city_id):
        """
        双向绑定关系解除接口

        :param bind_id: 绑定ID  双方号码+中间号绑定ID，该ID全局唯一
        :param city_id: 城市ID
        """
        body = {
            "appId": self.appId,
            # "requestId": "111",
            "bindId": bind_id,
            "cityId": city_id
        }

        return self.send_http_request('safetyCalls', 'freeNumber', json.dumps(body))

    def tw_bn_sync(self, caller, callee, city_id):
        """
        双向绑定号码同步接口

        :param caller: 主叫号码
        :param callee: 被叫号码
        :param city_id: 城市ID
        """
        body = {
            "hangupUrl": "",
            "caller": caller,
            "appId": self.appId,
            "callerRingName": "a.mp3",
            "bindId": "7df01234567841ed816564bb12345678",
            "requestId": "111111",
            "calleeDisplayNum": "0086221000123",
            "maxAge": "600",
            "record": "0",
            "maxAllowTime": "5",
            "dstVirtualNum": "0086221000123",
            "calleeRingName": "b.mp3",
            "statusUrl": "",
            "callee": callee,
            "recordUrl": "",
            "cityId": city_id
        }

        return self.send_http_request("safetyCalls", "applyNumber", json.dumps(body))

    def ow_bn_alloc(self, callee, city_id):
        """
        单向绑定号码申请接口

        :param callee: 被叫号码
        :param city_id: 城市ID
        """
        body = {
            "hangupUrl": "",
            "appId": self.appId,
            "requestId": "111111",
            "calleeDisplayNum": "0086221000123",
            "maxAge": "600",
            "record": "0",
            "maxAllowTime": "10",
            "dstVirtualNum": "0086221000123",
            "callerRingName": "b.mp3",
            "statusUrl": "",
            "callee": callee,
            "recordUrl": "",
            "cityId": city_id
        }

        return self.send_http_request("safetyCalls", "chooseNumber", json.dumps(body))

    def ow_bn_free(self, bind_id, city_id):
        """
        单向绑定关系解除接口

        :param bind_id: 绑定ID
        :param city_id: 城市ID
        """
        body = {
            "appId": self.appId,
            "bindId": bind_id,
            "cityId": city_id
        }

        return self.send_http_request('safetyCalls', 'unbindNumber', json.dumps(body))

    def get_concurrent(self, city_id="all"):
        """
        城市并发查询接口

        :param city_id: 城市ID
        """
        body = {
            "appId": self.appId,
            "cityId": city_id
        }

        return self.send_http_request('safetyCalls', 'getConcurrent', json.dumps(body))

    def template_sms(self, to_numbers, template_id, param):
        """
        短信验证码（模板短信）

        :param to_numbers: 被叫的号码
        :param template_id: 模板Id
        :param param: <可选> 内容数据，用于替换模板中{数字}
        """
        body = {
            "templateSMS": {
                "appId": self.appId,
                "param": param,
                "templateId": template_id,
                "to": to_numbers
            }
        }
        return self.send_http_request('Messages', 'templateSMS', json.dumps(body))


rest = YzxAPI()

"""
短信验证码发送接口
"""
#print(rest.template_sms('15655138143', 160320, 123))

"""
私密通话接口
"""

# 双向绑定号码同步接口
# resp = rest.tw_bn_sync(caller_num, callee_num, city_id)
# print resp

# 双向绑定关系解除接口
# print(rest.tw_bn_free(resp["bindId"], city_id))

# 双向绑定号码申请接口
# resp = rest.tw_bn_alloc(caller_num, callee_num, city_id)
# print resp

# 双向绑定关系解除接口
# print(rest.tw_bn_free("b172ad7497db43f687716ce112b028d9", city_id))
# print(rest.tw_bn_free(resp["bindId"], city_id))

# 单向绑定号码申请接口
# resp = rest.ow_bn_alloc(callee_num, city_id)
# print resp

# 单向绑定关系解除接口
# print(rest.ow_bn_free(resp["bindId"], city_id))

# 城市并发查询接口
# print(rest.get_concurrent())

#resp = rest.tw_bn_alloc("008615655138143", "008615921439674", "008621")
#print(resp)
#print()
#print(rest.get_concurrent())
