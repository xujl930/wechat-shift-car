# -*- coding:utf8 -*-
from flask import session, render_template
from app.models.model import User
import functools

def has_user_openid(openid):
    user = User.query.filter_by(openid=openid).first()
    if not user:
        return None
    return user

def set_user(user_info):
    session['wechat_user_id'] = user_info['openid']
    session['wechat_user_header'] = user_info['headimgurl']
    session['wechat_user_nickname'] = user_info['nickname']

def check_user():
    return session.get('wechat_user_id')

def register_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        openid = session.get('wechat_user_id')
        caller = User.query.filter_by(openid= openid).first()
        if not caller:
            return render_template('register.html')

