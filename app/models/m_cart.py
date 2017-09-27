from marshmallow_jsonapi import Schema, fields
from marshmallow import validate, pprint
from sqlalchemy import func
from sqlalchemy.orm import relationship, mapper
from sqlalchemy.exc import SQLAlchemyError
from app import CRUD
from app import db

from app.models.m_products import s_product
from app.models.m_address import s_address
from app.models.m_users import s_user
from app.models.m_bank import s_bank
# from app.models.m_order import t_order, s_order

# table akan terbuat jika file ini sudah di import di view
class t_cart(db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    id_order    = db.Column(db.Integer, db.ForeignKey('t_order.id'))
    id_user     = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    id_product  = db.Column(db.Integer, db.ForeignKey('t_product.id'))
    jml_product = db.Column(db.Integer, nullable=False)
    cart_status = db.Column(db.Boolean, default=False, nullable=True)
    createDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    rel_user    = db.relationship("t_user", backref=db.backref("t_cart", lazy="dynamic"))     #harus ada ini untuk relasi dan ambil data dari table terelasi
    rel_product = db.relationship("t_product", backref=db.backref("t_cart", lazy="dynamic"))
    rel_order   = db.relationship("t_order", backref=db.backref("t_cart", lazy="dynamic"))

    def __init__(self, id, id_user, id_order, id_product, jml_product):
        self.id         = id
        self.id_user    = id_user 
        self.id_order   = id_order
        self.id_product = id_product
        self.jml_product= jml_product

class s_cart(Schema):
    id          = fields.Integer(dump_only=True)
    jml_product = fields.Integer()
    rel_product = fields.Nested(s_product, only=('id','product_nm','product_price','product_color','product_img')) #get data product from rel_product
    # rel_order   = fields.Nested(s_order)
    rel_user    = fields.Nested(s_user)

    class Meta:
        type_ = 'cart'