# -*- coding:utf8 -*-
from flask import Blueprint, url_for

api = Blueprint('api', __name__)
page = Blueprint('page', __name__)

from . import routes, api1_0

# 初始化公众号菜单
routes.create_menu()