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
from app.models.m_products import s_product

# to make auto number invoice
def increment_invoice():
    last_invoice = db.session.query(func.max(t_order.id)).one()[0]
    if last_invoice == None:
        return 'INV00000001'
    jarak = 8
    new_invoice_int = last_invoice + 1
    new_formated = (jarak - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
    new_no_invoice = 'INV' + str(new_formated)
    return new_no_invoice

class t_order(db.Model, CRUD):
    id              = db.Column(db.Integer, primary_key=True)
    no_invoice      = db.Column(db.String(15), nullable=False)
    id_user         = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    status_order    = db.Column(db.Enum('verifikasi','dikirim','diterima','dibatalkan', name='status'), default='verifikasi', nullable=True)
    payment_to_bank = db.Column(db.Integer, db.ForeignKey('t_bank.id'), nullable=True)
    shipping        = db.Column(db.Integer, nullable=True)
    total_order     = db.Column(db.Integer, nullable=True)
    isVisible       = db.Column(db.Boolean, default=False, nullable=True)
    id_address      = db.Column(db.Integer, db.ForeignKey('t_address.id'))
    createDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate      = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    rel_order_detail= db.relationship('t_item_order', backref=db.backref('t_order'))
    rel_user        = db.relationship('t_user', backref=db.backref('t_order', lazy='dynamic'))
    rel_bank        = db.relationship('t_bank', backref=db.backref('t_order', lazy='dynamic'))
    rel_address     = db.relationship('t_address', backref=db.backref('t_order', lazy='dynamic'))

    def __init__(self, id, no_invoice, id_user, payment_to_bank, id_address, shipping, total_order):
        self.id                 = id
        self.no_invoice         = no_invoice
        self.id_user            = id_user
        self.payment_to_bank    = payment_to_bank
        self.id_address         = id_address
        self.shipping           = shipping
        self.total_order        = total_order

class s_order(Schema):
    id              = fields.Integer(dump_only=True)
    no_invoice      = fields.String()
    shipping        = fields.Integer()
    total_order     = fields.Integer()
    status_order    = fields.String()
    isVisible       = fields.Boolean()
    rel_order_detail= fields.Nested('s_item_order', many=True)   #many=True untuk ambil data lewat primary key t_order ke t_cart
    rel_user        = fields.Nested(s_user)
    rel_bank        = fields.Nested(s_bank)
    rel_address     = fields.Nested(s_address)
    createDate      = fields.Date()
    updateDate      = fields.Date()
    class Meta:
        type_ ='order'

class t_item_order(db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    id_order    = db.Column(db.Integer, db.ForeignKey('t_order.id'))
    id_product  = db.Column(db.Integer, db.ForeignKey('t_product.id'))
    jml_product = db.Column(db.Integer, nullable=False)
    createDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    rel_product = db.relationship("t_product", backref=db.backref("t_cart", lazy="dynamic"))
    
    def __init__(self, id, id_user, id_order, id_product, jml_product):
        self.id         = id
        self.id_user    = id_user 
        self.id_order   = id_order
        self.id_product = id_product
        self.jml_product= jml_product

class s_item_order(Schema):
    id          = fields.Integer(dump_only=True)
    jml_product = fields.Integer()
    rel_product = fields.Nested(s_product, only=('id','product_nm','product_price','product_color','product_img')) #get data product from rel_product
    
    class Meta:
        type_ = 'item_order'