# -*- coding:utf8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wechatpy import Wechat
from flask_login import LoginManager
from flask_session import Session
from config import config

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatJSAPI

db = SQLAlchemy()
wechat = Wechat()
#session = Session()
