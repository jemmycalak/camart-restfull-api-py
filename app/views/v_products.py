from flask import Blueprint, request, jsonify, make_response
from app import db
from flask_restful import Api, Resource
from sqlalchemy import func, sql, update, join
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import join
from marshmallow import ValidationError
import re, datetime, json, dateutil.parser
from datetime import date, datetime
from app.util.firebase_notification import push_notification

from app.models.m_products import t_product, s_product, t_category, s_category
from app.models.m_cart import t_cart, s_cart
from app.models.m_order import t_order, s_order, increment_invoice, t_item_order
from app.models.m_users import t_user, s_user
from app.models.m_buktiPembayaran import t_buktiPembayaran, s_buktiPembayaran
# import psycopg2
# from config
from types import *
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

        try:
            sql = t_product.query.all()
            data = s_product().dump(sql, many=True).data
            result = {'status':'true', 'msg':data}, 200

        except Exception as err:
            print err
            result = {'status':'false', 'msg':'Tidak dapat mengambil data'}, 401
        return result

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

        dt_cat= data
        result={'status':'true', 'data':dt_cat}, 200
        return result

class cart(Resource):
    def post(self):

        id_user_rw = request.json.get("id_user")
        print id_user_rw

        sql = t_cart.query.filter_by(id_user=id_user_rw).all()

        if len(sql) > 0:
            data_cart = s_cart().dump(sql, many=True).data
            #make a structure json
            # data=[]
            # for i in range(len(data_cart['data'])):
            #     data.insert(i,{
            #         'id'            :data_cart['data'][i]['id'],
            #         'id_user'       :data_cart['data'][i]['attributes']['id_user'],
            #         'status_cart'   :data_cart['data'][i]['attributes']['cart_status'],
            #         'product_img'   :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_img'],
            #         'product_nm'    :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_nm'],
            #         'product_price' :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_price'],
            #         'product_color' :data_cart['data'][i]['attributes']['rel_product']['data']['attributes']['product_color']
            #     })

            # data_cart = data
            resp= {'status':'true', 'data':data_cart}
        else:
            resp = {'status':'false', 'data':'empty cart'}, 200
        return resp

class order_detail(Resource):
    def post(self):

        id_user_rw = request.json.get("id_user")
        sql = t_order.query.filter_by(id_user = id_user_rw ).all()
        if len(sql) > 0:
            dt_order = s_order().dump(sql, many=True).data
            data = []
            for i in range(len(dt_order['data'])):
                data.insert(i, {
                    'id_order'      : dt_order['data'][i]['id'],
                    'no_invoice'    : dt_order['data'][i]['attributes']['no_invoice'],
                    'stts_order'    : dt_order['data'][i]['attributes']['status_order'],
                    'shipping'      : dt_order['data'][i]['attributes']['shipping'],
                    'tgl_order'     : dt_order['data'][i]['attributes']['createDate'],
                    'total_order'   : dt_order['data'][i]['attributes']['total_order'],
                    'isVisible'     : dt_order['data'][i]['attributes']['isVisible'],
                    'penerima'      : dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['nm_penerima'],
                    'almt_penerima' : dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['alamat'],
                    'province'      : dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['province'],
                    'notelp_penerima':dt_order['data'][i]['attributes']['rel_address']['data']['attributes']['notelp_penerima'],
                    'payment_to'    : dt_order['data'][i]['attributes']['rel_bank']['data']['attributes']['nm_bank'],
                    'payment_to_rek': dt_order['data'][i]['attributes']['rel_bank']['data']['attributes']['norek'],
                    'order_detail'  : dt_order['data'][i]['attributes']['rel_order_detail']['data']
                    #     'product': data1 = []
                    #     for j in range(len(dt_order['data'][i]['attributes']['rel_order_detail']['data'])):
                    #         data1.insert(j,{
                    #             'product_id'  : dt_order['data'][i]['attributes']['rel_order_detail']['data'][j]['attributes']
                    #         })
                    # }

                    # 'order_detail'  : dt_order['data'][i]['attributes']['rel_order_detail']['data'][i]['attributes']
                    # {
                    #     for j in range(len(dt_order['data'][i]['attributes']['rel_order_detail']['data'])):
                    #         'product_id'    : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data'][j]['id']
                    # }
                    # {
                    #     'product_id'    : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['id'],
                    #     'product_nm'    : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_nm'],
                    #     'product_color' : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_color'],
                    #     'product_price' : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_price'],
                    #     'product_img'   : dt_order['data'][i]['attributes']['rel_order_detail']['data']['attributes']['rel_product']['data']['attributes']['product_img']
                        
                    # }
                })


            dt_order=data
            resp = {'status':'true', 'data':dt_order}, 200
        else:
            resp = {'status':'false', 'data':'empty data order'}, 200

        return resp

class order_product(Resource):
    def post(self):
        
        req = request.json.get
        # to insert table order
        id_user = req("id_user")
        id_bank = req("id_bank")
        shiping = req("shiping")
        total   = req("total")
        id_addr = req("id_address")

        # to insert item_order
        barang = req("product")

        # print id_user, id_bank, shiping, total, id_addr, barang
        
        try:
            # get id order
            lastidorder = db.session.query(func.max(t_order.id)).one()[0]
            if lastidorder == None:
                lastidorder = 0
            id_order = int(lastidorder)+1
            # print id_order

            # get no_invoice
            no_invoice = increment_invoice()
            # print "aaaaa", no_invoice
    
            # do insert to table order
            insert_order = t_order(id_order, no_invoice, id_user, id_bank, id_addr, shiping, total)
            insert_order.add(insert_order)

            # convert from unicode type to json type
            if type(barang) is UnicodeType:
                barang = json.loads(barang)
    
            for data in barang:
                id_barang   = data['id_product'] 
                jmlah_barang= data['jumlah'] 
                # print id_barang, jmlah_barang

                # get id item
                lastiditem = db.session.query(func.max(t_item_order.id)).one()[0]
                if lastiditem == None:
                    lastiditem = 0
                id_item = int(lastiditem)+1
                # print id_item
                

                #insert
                insert_item = t_item_order(id_item, id_user, id_order, id_barang, jmlah_barang)
                insert_item.add(insert_item)
            
    
            t_firebase = db.session.query(t_user.token_firebase).filter_by(id= id_user).one()[0]
            message = "Anda tinggal melakukan pembayaran (0_0)"
            push_notification(t_firebase, message)
            resp = {"status":"true","msg":"order success"}, 200
        except Exception as err:
            resp = {"status":"false", "msg":"order faild"}, 404
        
        return resp
        
class cancleorder(Resource):
    def post(self):
        req = request.json.get

        id_user_raw = req("id_user")
        no_invoice_raw = req("no_invoice")
        print id_user_raw, no_invoice_raw

        try:
            sql = db.session.query(t_order).filter_by(id_user = id_user_raw).filter_by(no_invoice = no_invoice_raw).update({"status_order":"dibatalkan"})
            db.session.commit()

            t_firebase = db.session.query(t_user.token_firebase).filter_by(id= id_user_raw).one()[0]
            message = "Kami merasa sedih anda membatalkan pesanan (T_T)"
            push_notification(t_firebase, message)
            resp = {"success":"true", "msg":"berhasil cancle order"}, 200
        except Exception as err:
            resp = {"success":"false", "msg":"gagal cancle order"}, 401

        return resp

# ='/api/v1/products'
api.add_resource(show_products, '/products')
api.add_resource(category, '/category')
api.add_resource(cart, '/cart')
api.add_resource(order_product, '/order')
api.add_resource(order_detail, '/orderdetail')
api.add_resource(cancleorder, '/cancleorder')