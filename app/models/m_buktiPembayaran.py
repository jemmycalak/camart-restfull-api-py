from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from app import CRUD
from app import db

from app.models.m_order import s_order

class t_buktiPembayaran(db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    id_order    = db.Column(db.Integer, db.ForeignKey('t_order.id'))
    img_url     = db.Column(db.TEXT, nullable=False)
    createDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    rel_order   = db.relationship('t_order', backref=db.backref('t_buktiPembayaran', lazy='dynamic'))

    def __init__(self, id, id_order, img_url):
        self.id         = id
        self.id_order   = id_order
        self.img_url    = img_url

class s_buktiPembayaran(Schema):
    id          = fields.Integer(dump_only = True)
    img_url     = fields.String()
    rel_order   = fields.Nested(s_order)
    createDate  = fields.Date()
    updateDate  = fields.Date()
    class Meta:
        type_ = 'buktiPemabayaran'
    