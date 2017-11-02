# -*- coding:utf8 -*-
from flask_login import UserMixin
from app.extent import  db
import uuid


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), unique=True, index=True)
    openid = db.Column(db.String(32), unique=True, index=True)
    car_num = db.Column(db.String(10), unique=True)
    head_pic = db.Column(db.String(64), nullable=True)
    uuid = db.Column(db.String(32), default=lambda: str(uuid.uuid4()).replace('-', '').strip())
    qrcodes = db.relationship('QrCode', backref='user', cascade='all,delete', lazy='dynamic')

    def __init__(self, phone, openid, car_num=None, head_pic=None):
        self.phone = phone
        self.openid = openid
        self.car_num = car_num
        self.head_pic = head_pic

    def to_json(self):
        json_user = {
            'id': self.id,
            'phone': self.phone,
            'openid': self.openid,
            'car_num': self.car_num,
            'head_pic': self.head_pic,
            'uuid': self.uuid
        }
        return json_user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.openid

    def __repr__(self):
        return '<User %r>' % (self.openid)

class QrCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #qr_content = db.Column(db.String(64), unique=True)
    qr_path = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.openid'))


    def __init__(self, qr_path, user_id, qr_content=None):
        self.qr_path = qr_path
        self.user_id = user_id
        self.qr_content = qr_content

    def to_json(self):
        json_code = {
            'id': self.id,
            'qr_path': self.qr_path,
            'user_id': self.user_id
          }
        return json_code