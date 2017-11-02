# -*- coding:utf8 -*-
import datetime
import random
import string
from app.extent import db, wechat
from app.models.model import User, QrCode
from app.utils.yunzhixun_utils import YzxAPI
from config import Config
from flask import session, jsonify, request, render_template

from . import api
from .routes import generate_qrcode

rest = YzxAPI()


@api.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok'})


# 获取短信验证码
@api.route('/getcode', methods=['POST'])
def get_code():
    phone = request.form.get('phone', None)
    # phone = request.get_json('phone', None)#['phone']
    if not phone:
        return 'failed'
    message_code = rest.get_message_code()
    if session.get(phone):
        session.pop(phone)

    session[phone] = message_code
    print(phone)

    r = rest.template_sms(to_numbers=phone, template_id=160320, param=message_code)
    rcode = r.get('resp').get('respCode')
    if rcode:
        # print(rcode)
        return rcode
    else:
        return 'failed'


# 双向绑定虚拟号码
@api.route('/call', methods=['POST'])
def connect_call():
    callout = request.form.get('caller')
    callin = request.form.get('callee')
    if callout and callin:
        caller = '0086' + callout
        callee = '0086' + callin
        city_id = '008621'

        resp = rest.tw_bn_alloc(caller=caller, callee=callee, city_id=city_id)
        print(resp)
        virnum = resp.get('dstVirtualNum')
        errorcode = resp.get('errorCode')
        if errorcode:
            print(errorcode)
            return '绑定虚拟号失败'
        return virnum
    else:
        return '获取号码失败'


# 更新用户信息
@api.route('/user/update', methods=['POST'])
def update_user():
    car_num = request.form.get('car_num')
    phone = request.form.get('phone_num')
    print(car_num + '\n' + phone)

    if not car_num or not phone:
        return 'null info'

    openid = session.get('wechat_user_id')
    # print(openid)
    user = User.query.filter_by(openid=openid).first()
    if not user:
        return render_template('404.html', error='查找用户不存在'), 404
    user.car_num = car_num
    user.phone = phone
    # print(user.qrcodes.all())
    # print(user.qrcodes.first())
    if not user.qrcodes.first():
        # return render_template('404.html', error= '该用户二维码不存在')
        generate_qrcode(openid=openid)
    db.session.commit()
    return '更新成功'


# 微信jssdk验证接口
@api.route('/jssdk', methods=['POST'])
def jssdk():
    if request.method == 'POST':
        try:
            url = request.form.get('url')
        except Exception:
            return 'error json format', 400

        appid = Config.WECHAT_APPID
        noncestr = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        timestamp = int(datetime.datetime.now().timestamp())
        # 从wechatpy中获取jsapi对象
        jsapi = wechat.__getattr__('jsapi')
        ticket = jsapi.get_jsapi_ticket()

        signature = jsapi.get_jsapi_signature(noncestr=noncestr, ticket=ticket,
                                              timestamp=timestamp, url=url)
        data = {
            'appId': appid,
            'timestamp': timestamp,
            'nonceStr': noncestr,
            'signature': signature
        }
        # print(data)
        # print(wechat.fetch_access_token())
        return jsonify({'data': data})


# 对用户和二维码操作接口（测试）
@api.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for u in users:
        user_list.append(u.to_json())
    return jsonify(user_list)


@api.route('/code', methods=['GET'])
def get_all_codes():
    codes = QrCode.query.all()
    code_list = []
    for c in codes:
        code_list.append(c.to_json())
    return jsonify(code_list)


@api.route('/user/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def get_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(user.to_json())
    # if request.method == 'PATCH':
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return 'delete user '+user.openid +' ok'


@api.route('/code/<int:id>', methods=['GET', 'DELETE'])
def code(id):
    code = QrCode.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(code.to_json())
    if request.method == 'DELETE':
        db.session.delete(code)
        db.session.commit()
        return 'delete qrcode '+code.user_id+' ok'
