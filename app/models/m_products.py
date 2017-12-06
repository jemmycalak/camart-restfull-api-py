from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app import CRUD
from app import db
from sqlalchemy.orm import relationship

class t_category(db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key = True)
    nm_cat      = db.Column(db.String(50), nullable = False)
    img_cat     = db.Column(db.TEXT, nullable = False)
    createDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    isDelete    = db.Column(db.Boolean, default=False, nullable=True)
    
    def __init__(self, id, nm_cat, img_cat):
        self.id = id
        self.nm_cat = nm_cat
        self.img_cat = img_cat

class s_category(Schema):
    id      = fields.Integer(dump_only=True)
    nm_cat  = fields.String()
    img_cat = fields.String()

    class Meta:
        type_ = 'category'

# table akan terbuat jika file ini sudah di import di view
class t_product(db.Model, CRUD):
    id              = db.Column(db.Integer, primary_key=True)
    product_nm      = db.Column(db.String(200), nullable=False)
    product_price   = db.Column(db.Integer, nullable=False)
    product_desc    = db.Column(db.String(700), nullable = True)
    product_weight  = db.Column(db.Integer, nullable=True)
    product_color   = db.Column(db.String(10), nullable=True)
    product_img     = db.Column(db.TEXT, nullable=False)
    product_stock   = db.Column(db.String(15), nullable=True)
    product_category= db.Column(db.Integer, db.ForeignKey('t_category.id'))
    createDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    isDelete        = db.Column(db.Boolean, default=False, nullable=True)
    rel_category    = db.relationship('t_category', backref=db.backref("t_product", lazy='joined'))

    def __init__(self, id, product_nm, product_price, product_desc, product_weight, product_color, product_img, product_stock, product_category ):
        self.id = id
        self.product_nm = product_nm
        self.product_price = product_price
        self.product_desc = product_desc
        self.product_weight = product_weight
        self.product_color = product_color
        self.product_img = product_img
        self.product_stock = product_stock
        self.product_category = product_category
        
class s_product(Schema):
    id              = fields.Integer(dump_only=True)
    product_nm      = fields.String()
    product_price   = fields.Integer()
    product_desc    = fields.String()
    product_weight  = fields.Integer()
    product_color   = fields.String()
    product_img     = fields.String()
    product_stock   = fields.String()
    rel_category    = fields.Nested(s_category, only=('id','nm_cat'))

    class Meta:
        type_ = 'products'