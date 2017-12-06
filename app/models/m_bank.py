from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from app import CRUD
from app import db

class t_bank(db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    nm_bank     = db.Column(db.String(15), nullable=False)
    norek       = db.Column(db.String(35), nullable=False)
    img_bank    = db.Column(db.String(150), nullable=False)
    atasnama     = db.Column(db.String(100), nullable=False)
    createDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    updateDate  = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)
    isDelete    = db.Column(db.TIMESTAMP, default=func.now(), nullable=True)

    def __init__(self, id, nm_bank, norek, img_bank, atasnama):
        self.id         = id
        self.nm_bank    = nm_bank
        self.img_bank   = img_bank
        self.atasnama   = atasnama

class s_bank(Schema):
    id      = fields.Integer(dump_only=True)
    nm_bank = fields.String()
    norek   = fields.String()
    img_bank= fields.String()
    atasnama= fields.String()

    class Meta:
        type_ ="banks"

