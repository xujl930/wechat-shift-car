# -*- coding:utf8 -*-
import os
from . import page
from flask import url_for, session, request, render_template, abort
from flask_wechatpy import oauth, wechat_required
from app.extent import db, wechat
from app.utils.wechat_utils import check_user, set_user, has_user_openid
from app.utils.qr_code import QrCode as QRCode
from app.models.model import User, QrCode
from config import Config
from wechatpy.replies import TextReply
from wechatpy.replies import create_reply


# 与微信服务器通信接口
@page.route('/check', methods=['GET', 'POST'])
@wechat_required    # 装饰器，用来校验来自微信服务器的信息，并建立其与公众号之间的通信
def check():
    msg = request.wechat_msg
    event_type = msg.type
    print(type(msg))
    print(msg.type)

    reply = TextReply(content='谢谢!', message=msg)
    if event_type == 'text':
        reply = create_reply(msg.content, message=msg)
    elif event_type == 'image':
        reply = TextReply(content='已收到图片!', message=msg)
    elif event_type == 'event':
        event = msg.event
        if event == 'subscribe':
            reply = TextReply(content=Config.WELCOME_TEXT, message=msg)
        elif event == 'click':
            key = msg.key
            if key == 'CALL_OWNER_BY_PLATE':
                reply = TextReply(content='抱歉,该功能目前暂未开放!', message=msg)
            elif key == 'V1001_GOOD':
                reply = TextReply(content='感谢您的支持!', message=msg)
        else:
            reply = TextReply(content='default', message=msg)
    else:
        reply = TextReply(content='谢谢反馈!', message=msg)
    return reply


# 更新公众号菜单（初始化调用）
@page.route('/menu', methods=['GET'])
def create_menu():
    menu = wechat.__getattr__('menu')
    if menu.get():
        menu.delete()
        menu.create(Config.MENU_SETTING)
    else:
        menu.create(Config.MENU_SETTING)
    return 'create menu ok'


# jssdk扫描二维码
@page.route('/scancode', methods=['GET'])
def scan_code():
    return render_template('scan_qrcode.html')


# jssdk接口示例
@page.route('/plate', methods=['GET'])
def plate():
    return render_template('photoPlate.html')


@page.route('/')
@oauth(check_func=check_user, set_user=set_user, scope='snsapi_userinfo')
def index():
    openid = session.get('wechat_user_id')
    print(openid)
    print(session.get('wechat_user_header'))
    print(session.get('wechat_user_nickname'))

    if not openid:
        return '<h1>授权失败!</h1>'

    user = has_user_openid(openid)
    if not user:
        return render_template('register.html')
    else:
        # print('uuid is: '+user.uuid)
        return render_template('dashboard.html', user=user)
        # return redirect(url_for('page.dashboard'))


@page.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    openid = session.get('wechat_user_id')
    phone = request.form['cellphone']
    code = request.form['code']

    user_phone = User.query.filter_by(phone=phone).first()
    if user_phone:
        return render_template('dashboard.html', user=user_phone)

    sess_code = session.get(phone)
    if not sess_code:
        return "<h1>验证码无效!</h1>"
    if code.strip() == str(sess_code).strip():
        user = User(phone=phone, openid=openid, head_pic=session.get('wechat_user_header'))
        db.session.add(user)

        session.pop(phone)  # 清除掉缓存中的验证码
        generate_qrcode(openid)  # 生成用户二维码
        db.session.commit()

        # 判断是否是由扫码，未注册用户跳转过来
        flag1 = session.get('caller-{0}'.format(openid))
        flag2 = session.get('callee-uuid')
        if flag1 and flag2:
            callee = User.query.filter_by(uuid=flag2).first()
            session.pop('caller-{0}'.format(openid))
            session.pop('callee-uuid')
            if not callee:
                abort(404)
            # print(user)
            # print(callee)
            return render_template('index.html', caller=user, callee=callee)
        else:
            return render_template('dashboard.html', user=user)
    else:
        return "<h1>验证码不匹配!</h1>"


# 用户主页
@page.route('/dashboard', methods=['GET'])
def dashboard():
    openid = session.get('wechat_user_id')
    user = has_user_openid(openid)
    return render_template('dashboard.html', user=user)


# 用户二维码入口
@page.route('/call/<uuid>')
@oauth(check_func=check_user, set_user=set_user, scope='snsapi_userinfo')
def call(uuid):
    openid = session.get('wechat_user_id')
    caller = User.query.filter_by(openid=openid).first()
    callee = User.query.filter_by(uuid=uuid).first()

    if not callee:
        return render_template('404.html', error='用户不存在 or 用户二维码已更新'), 404

    if not caller:
        session['caller-{0}'.format(openid)] = '1'
        session['callee-uuid'] = uuid
        return render_template('register.html')

    if caller.phone == callee.phone:
        session['wechat_user_id'] = callee.openid
        return render_template('dashboard.html', user=caller)
    return render_template('index.html', callee=callee, caller=caller)


# 清除用户session
@page.route('/clear')
def clear():
    if 'wechat_user_id' in session:
        session.pop('wechat_user_id')
    return "ok"


@page.route('/access_token')
def access_token():
    return "access token: {}".format(wechat.access_token)
    # return 'token'


# 生成用户信息二维码
def generate_qrcode(openid):
    user = User.query.filter_by(openid=openid).first()
    if not user:
        return render_template('404.html', error='查找用户失败，无法生成二维码'), 404
    content = os.path.join(Config.MAIN_URL + '/', 'call/' + user.uuid)
    local_path = os.path.join(Config.QRCODE_FOLDER, user.openid + '.png')
    url_path = url_for('static', filename='img/qrcode/' + user.openid + '.png', _external=True)
    # print(local_path)
    # print(url_path)
    QRCode.make_qr(content, local_path)
    qrcode = QrCode(qr_path=url_path, user_id=user.openid)
    db.session.add(qrcode)
    db.session.commit()


# # 校验来自微信服务器的验证（配置服务器时用）
# @page.route('/check', methods = ['POST'])
# def check_sig():
#     token = 'weixin'
#     timestamp = request.args.get('timestamp', '')
#     nonce = request.args.get('nonce', '')
#     signature = request.args.get('signature', '')
#     echostr = request.args.get('echostr', '')
#
#     checkArr = [token, timestamp, nonce]
#     checkArr.sort()
#     strArr = ''
#     for s in checkArr:
#         strArr += s
#
#     shastr = _sha1.sha1(strArr.encode('utf-8'))
#     if shastr.hexdigest() == signature:
#         print('success' + ' ' + 'echostr= ' + echostr)
#         print(shastr.hexdigest())
#         # return jsonify({'echostr': echostr})
#         return echostr
#     else:
#         print(shastr.hexdigest())
#         return 'check failed'
