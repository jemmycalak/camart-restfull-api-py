from flask import Blueprint, request, jsonify, make_response
from app import db
from flask_restful import Api, Resource
from sqlalchemy import func, sql, update, join
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import join
from marshmallow import ValidationError
import re, datetime, json, dateutil.parser
from datetime import date, datetime

from app.models.m_products import t_product, s_product, t_category, s_category
from app.models.m_cart import t_cart, s_cart
from app.models.m_order import t_order, s_order
from app.models.m_users import t_user, s_user
# import psycopg2
# from config

# import random, os

# Blueprint
products = Blueprint('product', __name__)

# Schema
product_group_schema = s_product()
cart_group_schema = s_cart()
order_group_schema = s_order()

api = Api(products)

class show_products(Resource):
    def get(self):

        sql = t_product.query.all()

        data = s_product().dump(sql, many=True).data

        # print data

        return data

# class insert_product(Resource):
#     def post(self):
#         raw_dict= request.get_json(force=True)

#         try:
#             lastid = db.session.query(func.max(t_product.id)).one()[0]
#             if lastid == None: lastid=0
#             pro

class category(Resource):
    def get(self):

        sql = t_category.query.all()
        dt_cat= s_category().dump(sql, many=True).data
        data = []
        for i in range(len(dt_cat['data'])):
            data.insert(i, {
                'id'    : dt_cat['data'][i]['id'],
                'nm_cat': dt_cat['data'][i]['attributes']['nm_cat'],
                'img_cat': dt_cat['data'][i]['attributes']['img_cat']
            })

        dt_cat['data'] = data
        result=dt_cat
        return result, 200

class cart(Resource):
    def post(self):

        id_user_rw = request.json.get("id_user")
        print id_user_rw

        sql = t_cart.query.filter_by(id_user = id_user_rw).all()
        data_cart = s_cart().dump(sql, many=True).data

        #make a structure json
        data=[]
        for i in range(len(data_cart['data'])):
            data.insert(i,{
                'id'            :data_cart['data'][i]['id'],
                'id_user'       :data_cart['data'][i]['attributes']['id_user'],
                'product_img'   :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_img'],
                'product_nm'    :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_nm'],
                'product_price' :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_price'],
                'product_color' :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_color']     

            })

        data_cart['data'] = data
        return data_cart

class order(Resource):
    def get(self):
        sql = t_order.query.all()

        dt_order = s_order().dump(sql, many=True).data

        data = []
        for i in range(len(dt_order['data'])):
            data.insert(i, {
                'id_order'      : dt_order['data'][i]['id']
                # 'no_invoice'    : dt_order['data'][i]['attributes']['no_invoice'],
                # 'stts_order'    : dt_order['data'][i]['attributes']['status_order'],
                # 'shipping'      : dt_order['data'][i]['attributes']['shipping']
                # 'penerima'      : dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['nm_penerima'],
                # 'almt_penerima' : dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['alamat'],
                # 'province'      : dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['province'],
                # 'notelp_penerima':dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['notelp_penerima'],
                # 'payment_to'    : dt_order['data'][i]['attributes']['rel_bank']['data']['attributes']['nm_bank'],
                # 'payment_to_rek': dt_order['data'][i]['attributes']['rel_bank']['data']['attributes']['norek'],
                # 'order_detail'  : {
                #     'product_id'    : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['id'],
                #     'product_nm'    : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_nm'],
                #     'product_color' : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_color'],
                #     'product_price' : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_price'],
                #     'product_img'   : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_img']
                    
                # }
            })

            dt_order['data']=data

        return dt_order


api.add_resource(show_products, '/products')
api.add_resource(category, '/category')
api.add_resource(cart, '/cart')
api.add_resource(order, '/order')