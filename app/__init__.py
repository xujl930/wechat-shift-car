# -*- coding:utf8 -*-
from flask import Flask
from config import config
from .extent import db, wechat

def create_app(config_name):
    app = Flask(__name__, static_folder='static',)
    app.config.from_object(config[config_name])

    db.init_app(app)
    wechat.init_app(app)
    #session.init_app(app)
    from .api_1_0 import api as api_blueprint, page as page_blueprint
    app.register_blueprint(page_blueprint, url_prefix='')
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app



# 定时任务