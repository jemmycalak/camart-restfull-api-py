from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from sqlalchemy import func
from sqlalchemy.orm import relationship, mapper
from sqlalchemy.exc import SQLAlchemyError
from app import CRUD
from app import db
from app.models.m_users import s_user

s_users = s_user()

class t_address(db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    nm_penerima = db.Column(db.String(30), nullable=False)
    alamat      = db.Column(db.String(150), nullable=False)
    province    = db.Column(db.String(20), nullable=False)
    notelp_penerima= db.Column(db.String(14), nullable=True)
    id_user     = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    createDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    rel_user    = db.relationship('t_user', backref=db.backref('t_address', lazy='dynamic'))

    def __init__(self, id,nm_penerima, alamat, province, notelp_penerima, id_user):
        self.id         = id
        self.nm_penerima= nm_penerima
        self.alamat     = alamat
        self.province   = province
        self.notelp_penerima=notelp_penerima
        self.id_user    = id_user

class s_address(Schema):
    id          =fields.Integer(dump_only=True)
    nm_penerima =fields.String()
    alamat      =fields.String()
    province    =fields.String()
    notelp_penerima =fields.String()
    id_user     =fields.Integer()
    rel_user    =fields.Nested(s_users, only=('id', 'user_notelp', 'user_email'))

    class Meta:
        type_ = 'address'