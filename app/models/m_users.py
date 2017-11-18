from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from app import CRUD
from app import db 


# table akan terbuat jika file ini sudah di import di view
class t_user(db.Model, CRUD):
    id              = db.Column(db.Integer, primary_key=True)                #field pertama harus id,, gk boleh user_id atau apa pun
    user_email      = db.Column(db.String(100), nullable=False)
    user_pw         = db.Column(db.String(100), nullable=False)
    user_nm         = db.Column(db.String(100), nullable=False)
    user_jk         = db.Column(db.String(10), nullable=True)
    user_notelp     = db.Column(db.String(14), nullable=False)
    user_birthDate  = db.Column(db.DATE, nullable = True)
    token_firebase  = db.Column(db.Text, nullable=True)
    createDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    isActive        = db.Column(db.Boolean, default=False, nullable=True)
    isDelete        = db.Column(db.Boolean, default=False, nullable=True)
    rel_cart        = db.relationship('t_cart', backref='t_user', lazy ='dynamic')

    def __init__(self, id, user_email, user_pw, user_nm, user_jk, user_notelp, token_firebase):
        self.id = id
        self.user_email = user_email
        self.user_pw = user_pw
        self.user_nm = user_nm
        self.user_jk = user_jk
        self.user_notelp = user_notelp
        self.token_firebase = token_firebase

class s_user(Schema):
    id              = fields.Integer(dump_only=True)
    user_email      = fields.String()
    user_pw         = fields.String()
    user_nm         = fields.String()
    user_jk         = fields.String()
    user_notelp     = fields.String()
    user_birthDate  = fields.Date()
    token_firebase  = fields.String()

    class Meta:
        type_ = 'users'