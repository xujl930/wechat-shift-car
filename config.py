# -*- coding:utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MAIN_URL = 'http://wechat-sport-dbg.huangloong.com'

    QRCODE_FOLDER = os.path.dirname(__file__)+os.path.sep+'app'+\
                    os.path.sep+'static'+os.path.sep+'img'+\
                    os.path.sep+'qrcode'


    # wechatpy 参数配置
    WECHAT_APPID = 'wxd3b8dba08fd21ad8'
    WECHAT_SECRET = '2a161dca8732a55af306b56c8b1868e1'
    WECHAT_TOKEN = 'weixin'
    WECHAT_SESSION_TYPE = 'redis'
    WECHAT_SESSTION_REDIS_URL = 'redis://localhost:6379/0'

    # flask-session
    # SESSION_TYPE = 'redis'

    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xa4T#\x95^?\xd7\xcc\xed\x00\x1b\xb2\xb7+@9{\xe7\xd8\x92A\xf5\xf0'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # 云之讯参数
    # YZX_URL = 'https://api.ucpaas.com/{SoftVersion}/Accounts/{accountSid}/{function}/{operation}?sig={SigParameter}'
    YZX_URL = 'https://api.ucpaas.com/{0}/Accounts/{1}/{2}/{3}?sig={4}'
    YZX_VERSION = '2014-06-30'
    YZX_ACCOUNTSID = 'a83adf766c1d6d750004f1fd5f46f603'
    YZX_TOKEN = 'd7ff45302554603359259f915e5b31a5'
    YZX_APPID = 'a0563086723d444688d1e10fafe64bb0'
    YZX_SECRET_NUMBER = '17082124973'

    # 欢迎语
    WELCOME_TEXT = '欢迎关注黄龙物联网科技!'

    # 公众号菜单设置
    MENU_SETTING = {
                "button":[
                    {
                        "type":"view",
                        "name":"注册",
                        "url": MAIN_URL
                    },
                    {
                        "name": "挪车选项",
                        "sub_button":[
                            {
                                "type": "scancode_push",
                                "name": "扫码挪车",
                                "key": "CALL_OWNER_BY_CODE"
                            },
                            {
                                #"type": "pic_photo_or_album",
                                "type": "click",
                                "name": "扫车牌挪车",
                                "key": "CALL_OWNER_BY_PLATE"
                            }
                        ],
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"个人信息",
                                "url":MAIN_URL
                            },
                            {
                                "type":"view",
                                "name":"关于我们",
                                "url":"http://www.huangloong.com"
                            },
                            {
                                "type":"click",
                                "name":"赞一下",
                                "key":"V1001_GOOD"
                            }
                        ]
                    }
                ]}


    # 前端页面地址
    FRONT_URL = {
        'REGISTER' : 'http://192.168.56.112:32777/register.html',
        'DASHBOARD' : 'http://192.168.56.112:32777/dashboard.html',
        'CALLING' : 'http://192.168.56.112:32777/index.html',
    }



    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # FLASKY_POSTS_PER_PAGE = 20
    # FLASKY_FOLLOWERS_PER_PAGE = 50
    # FLASKY_COMMENTS_PER_PAGE = 30
    # FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    # @classmethod
    # def init_app(cls, app):
    #     Config.init_app(app)
    #
    #     # email errors to the administrators
    #     import logging
    #     from logging.handlers import SMTPHandler
    #     credentials = None
    #     secure = None
    #     if getattr(cls, 'MAIL_USERNAME', None) is not None:
    #         credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
    #         if getattr(cls, 'MAIL_USE_TLS', None):
    #             secure = ()
    #     mail_handler = SMTPHandler(
    #         mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
    #         fromaddr=cls.FLASKY_MAIL_SENDER,
    #         toaddrs=[cls.FLASKY_ADMIN],
    #         subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
    #         credentials=credentials,
    #         secure=secure)
    #     mail_handler.setLevel(logging.ERROR)
    #     app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 'heroku': HerokuConfig,
    # 'unix': UnixConfig,

    'default': DevelopmentConfig
}