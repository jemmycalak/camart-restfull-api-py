from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from app import CRUD
from app import db

from app.models.m_address import s_address
from app.models.m_users import s_user
from app.models.m_bank import s_bank
from app.models.m_cart import s_cart


class t_order(db.Model, CRUD):
    id              = db.Column(db.Integer, primary_key=True)
    no_invoice      = db.Column(db.String(15), nullable=False)
    id_user         = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    status_order    = db.Column(db.Boolean, default=False, nullable=True)
    payment_to_bank = db.Column(db.Integer, db.ForeignKey('t_bank.id'), nullable=True)
    shipping        = db.Column(db.Integer, nullable=True)
    id_address      = db.Column(db.Integer, db.ForeignKey('t_address.id'))
    createDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    rel_order_detail= db.relationship('t_cart', backref=db.backref('t_order'))
    rel_user        = db.relationship('t_user', backref=db.backref('t_order', lazy='dynamic'))
    rel_bank        = db.relationship('t_bank', backref=db.backref('t_order', lazy='dynamic'))
    rel_address     = db.relationship('t_address', backref=db.backref('t_order', lazy='dynamic'))

    def __init__(self, id, no_invoice, id_user, payment_to_bank, id_address, shipping):
        self.id                 = id
        self.no_invoice         = no_invoice
        self.id_user            = id_user
        self.payment_to_bank    = payment_to_bank
        self.id_address         = id_address
        self.shipping           = shipping


class s_order(Schema):
    id              = fields.Integer(dump_only=True)
    no_invoice      = fields.String()
    shipping        = fields.Integer()
    status_order    = fields.Boolean()
    # rel_order_detail= fields.Nested(s_cart, many=True)   #many=True untuk ambil data lewat primary key t_order ke t_cart
    # rel_user        = fields.Nested(s_user)
    # rel_bank        = fields.Nested(s_bank)
    # rel_address     = fields.Nested(s_address)
    
    class Meta:
        type_ ='order'