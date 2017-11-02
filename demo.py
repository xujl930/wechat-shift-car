# -*- coding:utf8 -*-

from flask import Flask, request, session, redirect, render_template
from flask_wechatpy import Wechat, wechat_required, oauth
from wechatpy.replies import TextReply
from wechatpy.replies import create_reply

app = Flask(__name__)
app.config['WECHAT_APPID'] = 'wxd3b8dba08fd21ad8'
app.config['WECHAT_SECRET'] = '2a161dca8732a55af306b56c8b1868e1'
app.config['WECHAT_TOKEN'] = 'wexin'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

wechat = Wechat(app)

@app.route('/')
@oauth(scope='snsapi_userinfo')
def index():
    openid = session.get('wechat_user_id')
    if not openid:
        return '授权失败'
    if True==True:
        #return redirect('http://192.168.56.112:32777/register.bak.html.bak', code=302)
        return render_template('register.html')

    else:
        return redirect('http://192.168.56.112:32777/dashboard.html', code=302)


@app.route('/clear')
def clear():
    if 'wechat_user_id' in session:
        session.pop('wechat_user_id')
    return "ok"


@app.route('/wechat', methods=['GET', 'POST'])
@wechat_required
def wechat_handler():
    msg = request.wechat_msg
    if msg.type == 'text':
        reply = create_reply(msg.content, message=msg)
    else:
        reply = TextReply(content='hello', message=msg)

    return reply


@app.route('/access_token')
def access_token():
    return "access token: {}".format(wechat.access_token)

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8000, debug=1)
    app.run()