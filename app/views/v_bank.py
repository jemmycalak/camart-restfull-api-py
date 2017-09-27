from flask import Flask, Blueprint, request, jsonify, make_response
from app.models.m_bank import t_bank, s_bank
from app import db
from flask_restful import Api, Resource
from sqlalchemy import func, sql
from marshmallow import ValidationError
# import re, datatime, json, dateutil.parser
from datetime import date, datetime

# Blueprint
banks = Blueprint('banks', __name__)

# Schema
bank_group_schema = s_bank()
api = Api(banks)

#Endpoint
class bank(Resource):
    def get(self):
        sql = t_bank.query.all()
        dt_bank = s_bank().dump(sql, many=True).data

        data =[]
        for i in range(len(dt_bank['data'])):
            data.insert(i,{
                'id'        : dt_bank['data'][i]['id'],
                'nm_bank'   : dt_bank['data'][i]['attributes']['nm_bank'],
                'norek'     : dt_bank['data'][i]['attributes']['norek'],
                'img_bank'  : dt_bank['data'][i]['attributes']['img_bank']
            })
        
        dt_bank['data'] = data
        return dt_bank

api.add_resource(bank, '')