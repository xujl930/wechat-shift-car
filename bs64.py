# -*- coding:utf8 -*-
import base64
from flask import jsonify
if __name__ == '__main__':
    data = {
        'appId': 'appid',
        'timestamp': 'timestamp',
        'nonceStr': 'nonceStr',
        'signature': 'signature'
    }

    print(data)

    # with open('C:/Users/xuJL/Desktop/timg.jpg', 'rb') as pic:
    #     bs_pic = base64.b64encode(pic.read())
    #     print(bs_pic)
