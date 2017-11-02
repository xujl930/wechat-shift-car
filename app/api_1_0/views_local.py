# -*- coding:utf8 -*-
import os, _sha1, random, string, datetime

from flask import url_for, session, jsonify, redirect, request, render_template, abort
from flask_login import login_user, logout_user, login_required
from flask_wechatpy import oauth, wechat_required
from app.extent import db, login_manager, wechat
from app.utils.yunzhixun_utils import YzxAPI
from app.utils.wechat_utils import *
from app.utils.qr_code import QrCode as QRCode
from app.models.model import User, QrCode
from config import Config

from wechatpy.replies import TextReply
from wechatpy.replies import create_reply

from . import api, page

openid = 'qwerasd'
message_code = 0
rest = YzxAPI()
# print(app)
# print(api)

@page.route('/plate', methods=['GET', 'POST'])
#@wechat_required
#@oauth(check_func=check_user, set_user=set_user, scope='snsapi_userinfo')
def plate():
    try:
        url = request.get_json().get('url')
    except Exception:
        return 'error json format'

    appid = Config.WECHAT_APPID
    nonceStr = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    timestamp = int(datetime.datetime.now().timestamp())
    # 从wechatpy中获取jsapi对象
    jsapi = wechat.__getattr__('jsapi')
    ticket = jsapi.get_jsapi_ticket()

    signature = jsapi.get_jsapi_signature(noncestr=nonceStr, ticket=ticket,
                                          timestamp=timestamp, url=url)

    data = {
        'appId': appid,
        'timestamp': timestamp,
        'nonceStr': nonceStr,
        'signature': signature
    }
    print(data)
    return render_template('photoPlate.html',data=jsonify(data))


# @login_manager.user_loader
# def load_user(openid):
#     user = User.query.filter_by(openid=openid).first()
#     return user
#
# @page.route('/login', methods=['GET', 'POST'])
# def login():
#     pass



@page.route('/')
#@oauth(check_func=check_user, set_user=set_user, scope='snsapi_userinfo')
def index():
    global openid
    openid = session.get('wechat_user_id')
    print(openid)
    print(session.get('wechat_user_header'))
    print(session.get('wechat_user_nickname'))

    print()

    # if not openid:
    #     return '授权失败'

    user = has_user_openid(openid)
    if not user:
        return render_template('register.html')
    else:
        return redirect(url_for('page.dashboard'))

@page.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    global openid
    openid = session.get('wechat_user_id')
    phone = request.form['cellphone']
    code = request.form['code']
    #print(type(code))
    #print(type(session[phone]))

    #print(phone+'  '+code)
    #print(session[phone])
    sess_code = session.get(phone)
    if not sess_code:
        return '验证码无效'
    if code.strip() == str(sess_code).strip():
        user = User(phone=phone, openid=openid, head_pic=session.get('wechat_user_header'))
        #user = User(phone=phone, openid='qwerasd', head_pic=session.get('wechat_user_header'))
        db.session.add(user)

        session.pop(phone)
        generate_qrcode(openid)

        db.session.commit()

        if not session.get('caller'):
            return redirect(url_for('page.dashboard',))
        else:
            session.pop('caller')
            return redirect(url_for('page.call'))
    return phone+'\n'+code

def generate_qrcode(openid):
    user = User.query.filter_by(openid=openid).first()
    if not user:
        return render_template('404.html', error= '查找用户失败，无法生成二维码'), 404
    print(user)
    content = os.path.join(Config.MAIN_URL+'/', 'call/'+ user.uuid)
    local_path = os.path.join(Config.QRCODE_FOLDER, user.openid+'.png')
    url_path = url_for('static', filename='img/qrcode/'+user.openid+'.png', _external=True)

    print(local_path)
    print(url_path)

    QRCode.make_qr(content, local_path)
    qrcode = QrCode(qr_path=url_path, user_id=user.openid)
    db.session.add(qrcode)
    db.session.commit()


@page.route('/dashboard', methods=['GET'])
def dashboard():
    global openid

    openid = session.get('wechat_user_id')
    user = has_user_openid(openid)
    # login_user(user=user, remember=True)
    return render_template('dashboard.html', user = user)


@page.route('/call/<uuid>')
#@oauth(check_func=check_user, set_user=set_user, scope='snsapi_userinfo')
def call(uuid):
    #caller = User.query.filter_by(openid=session.get('wechat_user_id')).first()
    caller = User.query.filter_by(openid='ogWpa1m15ysHapXeFzwFcZNvUMuQ').first()
    if not caller:
        session['caller'] = 'true'
        return redirect(url_for('page.register',))
    user = User.query.filter_by(uuid=uuid).first()

    if caller.phone == user.phone:
        session['wechat_user_id'] = user.openid
        return redirect(url_for('page.dashboard'))

    if not user:
        return 'user none'
    return render_template('index.html', user= user, caller= caller)

@page.route('/clear')
def clear():
    if 'wechat_user_id' in session:
        session.pop('wechat_user_id')
    return "ok"


@page.route('/access_token')
def access_token():
    return 'token'
    # return "access token: {}".format(wechat.access_token)

# 校验来自微信服务器的验证
@page.route('/check')
def check_sig():
    token = 'weixin'
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    signature = request.args.get('signature', '')
    echostr = request.args.get('echostr', '')

    checkArr = [token, timestamp, nonce]
    checkArr.sort()
    strArr = ''
    for s in checkArr:
        strArr += s

    shastr = _sha1.sha1(strArr.encode('utf-8'))
    if shastr.hexdigest() == signature:
        print('success' + ' ' + 'echostr= ' + echostr)
        print(shastr.hexdigest())
        #return jsonify({'echostr': echostr})
        return echostr
    else:
        print(shastr.hexdigest())
        return 'check failed'

@api.route('/')
def index():
    return 'api interface'

@api.route('/getcode', methods=['POST'])
def get_code():
    global message_code
    # phone = request.form['cellphone']
    # print(request.content_type)
    phone = request.form.get('phone', None)
    # phone = request.get_json('phone', None)#['phone']

    if not phone :
        return 'failed'
    message_code = rest.get_message_code()
    if session.get(phone):
        session.pop(phone)

    session[phone] = message_code
    print(phone)

    r = rest.template_sms(to_numbers=phone, template_id=160320, param=message_code)
    rcode = r.get('resp').get('respCode')
    if rcode:
        return rcode
    else:
        return 'failed'

    #return '000000'#+str(message_code)

@api.route('/call', methods=['POST'])
def connect_call():
    callout = request.form.get('caller')
    callin = request.form.get('callee')
    if callout and callin:
        caller = '0086'+callout
        callee = '0086'+callin
        city_id = '008621'

        resp = rest.tw_bn_alloc(caller=caller, callee=callee, city_id=city_id)
        virnum = resp.get('dstVirtualNum')
        errorcode = resp.get('errorCode')
        if errorcode:
            print(errorcode)
            return '绑定虚拟号失败'
        return virnum
    else:
        return '获取号码失败'


@api.route('/user/self', methods=['POST'])
def update_user():
    car_num = request.form.get('car_num')
    phone = request.form.get('phone_num')
    print(car_num+'\n'+phone)

    if not car_num or not phone:
        return 'null info'

    global openid
    # openid = request.cookies.get('openid')
    openid = session.get('wechat_user_id')
    print(openid)
    user = User.query.filter_by(openid=openid).first()
    if not user:
        return render_template('404.html', error= '查找用户不存在 Or 用户二维码已更新'), 404
    user.car_num = car_num
    user.phone = phone
    if not user.qrcodes[0]:
        generate_qrcode(openid=openid)
    db.session.commit()
    return '更新成功'

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
    #if request.method == 'PATCH':
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return 'delete ok'

@api.route('/code/<int:id>', methods=['GET', 'DELETE'])
def code(id):
    code = QrCode.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(code.to_json())
    if request.method == 'DELETE':
        db.session.delete(code)
        db.session.commit()
        return 'delete ok'
