from flask import Flask, Blueprint, request, jsonify, make_response
from app.models.m_users import t_user, s_user
import Crypto.Hash
from Crypto.Hash import SHA256
# from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from flask_restful import Api, Resource
from sqlalchemy import func, sql, update
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import re, datetime, json, dateutil.parser
from datetime import date, datetime
from app.views.sendEmail import senEmail
from app.models.m_address import t_address, s_address

#import random, os

#Blueprint
users = Blueprint('users', __name__)

#Schema
user_group_schema = s_user()
address_group_schema = s_address()

#nanti akan di panggil di __init__.py
api = Api(users)

class login(Resource):
    def post(self):
        
        email_rw = request.json.get("email")
        password_rw = request.json.get("password")
        print email_rw, password_rw

        # encrypt password
        pass_enc = encrypt(password_rw)
        # print pass_enc

        #query login
        sql = t_user.query.filter_by(user_email=email_rw).filter_by(user_pw=pass_enc).count()

        if not sql:
                #login failed
            resp = {'success' : 'false', 'msg': 'Login failed.' }
        else:
            # if sql > 0:
                  #get data after login  
            sql1 = db.session.query(
                t_user.id,
                t_user.user_email,
                t_user.user_pw,
                t_user.user_nm,
                t_user.user_jk,
                t_user.user_notelp,
                t_user.user_birthDate
            ).filter_by(user_email = email_rw)

            data_user = s_user().dump(sql1, many=True).data
            
            #make new structure json
            data_json = []
            for i in range(len(data_user['data'])):
                data1 = []
                data1.insert(i, {
                    'id'    :data_user['data'][i]['id'],
                    'email' :data_user['data'][i]['attributes']['user_email'],
                    'pw'    :data_user['data'][i]['attributes']['user_pw'],
                    'name'  :data_user['data'][i]['attributes']['user_nm'],
                    'jk'    :data_user['data'][i]['attributes']['user_jk'],
                    'notelp':data_user['data'][i]['attributes']['user_notelp']
                })
                for a in data1:
                    data_json.append(a)
                
            #replace data_user become data_json
            data_user=data_json

            resp = jsonify({'success' : 'true', 'msg': 'Login Success, Welcome.', 'data':data_user })
            
            # sentEml= senEmail(email_rw)             #send parameter
            # sentEml.oto()                           #run the method
        
        return resp

def encrypt(password):
    enc = SHA256.new()
    enc.update(password)
    pass_enc = enc.hexdigest()
    return pass_enc

class register(Resource):
    def post(self):
        nama_rw = request.json.get("nama")
        email_rw = request.json.get("email")
        password_rw = request.json.get("password")
        notelp_rw = request.json.get("notelp")
        jk_rw = request.json.get("jk")

        print nama_rw, email_rw, password_rw, notelp_rw, jk_rw

        # encrypt password
        pass_enc = encrypt(password_rw)

        # print nama_rw, email_rw, password_rw, notelp_rw, jk_rw

        try:
            chekEmail = t_user.query.filter_by(user_email = email_rw).count()
            if chekEmail > 0 :
                resp = {'status':'false', 'msg':'Email sudah digunakan.'}
            else :
                lastid = db.session.query(func.max(t_user.id)).one()[0]
                if lastid == None: 
                    lastid = 0
                id = int(lastid) + 1
                
                # if date == "00" and month == "00" and year == "0000" :
                #     date = "01"
                #     month = "01"
                #     year = "2000"
                
                # birthdate= year+'-'+month+'-'+date

                #insert data to db
                user = t_user(id, email_rw, pass_enc, nama_rw, jk_rw, notelp_rw)
                user.add(user)

                #get data from db
                getdata = db.session.query(
                    t_user.id,
                    t_user.user_nm,
                    t_user.user_email,
                    t_user.user_pw,
                    t_user.user_jk,
                    t_user.user_notelp
                ).filter_by(id = id)

                dataUser = s_user().dump(getdata, many = True).data
                
                #make new struktur json
                data1 = []
                for i in range(len(dataUser['data'])):
                    data2 = []
                    data2.insert(i, {
                        'id':       dataUser['data'][i]['id'],
                        'name':     dataUser['data'][i]['attributes']['user_nm'],
                        'email':    dataUser['data'][i]['attributes']['user_email'],
                        'jk':       dataUser['data'][i]['attributes']['user_jk'],
                        'notelp':   dataUser['data'][i]['attributes']['user_notelp']
                    })
                    #insert data to data1
                    for a in data2:
                        data1.append(a)
                
                #replace realdata to data1
                dataUser = data1

                sentEml= senEmail(email_rw)             #send parameter
                sentEml.oto()

                resp = {'status':'true', 'msg':'Selamat anda telah terdaftar.', 'data': dataUser}
        
        except Exception as err:
            resp = {'status':'false', 'msg':'Gagal mendaftarkan data.'}

        return resp

class address(Resource):
    def post(self):
        id_user_rw = request.json.get("id_user")

        sql= t_address.query.filter_by(id_user=id_user_rw).all()
        dt_address = s_address().dump(sql, many=True).data

        data = []
        for i in range(len(dt_address['data'])):
            data.insert(i,{
                'id'            :dt_address['data'][i]['id'],
                'nm_penerima'   :dt_address['data'][i]['attributes']['nm_penerima'],
                'notelp_penerima':dt_address['data'][i]['attributes']['notelp_penerima'],
                'alamat'        :dt_address['data'][i]['attributes']['alamat'],
                'province'      :dt_address['data'][i]['attributes']['province'],
                'id_user'       :dt_address['data'][i]['attributes']['id_user']

            })

        dt_address['data']=data

        return dt_address

api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(address, '/address')
