from flask import Flask, Blueprint, request, jsonify, make_response
from app.models.m_users import t_user, s_user
import Crypto.Hash
from Crypto.Hash import SHA256
import jwt
# from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from flask_restful import Api, Resource
from sqlalchemy import func, sql, update
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import re, datetime, json, dateutil.parser
from datetime import date, datetime, timedelta
from app.views.sendEmail import senEmail
from app.models.m_address import t_address, s_address
from app.util.firebase_notification import push_notification
from config import SECRET_KEY, JWT_EXP_DELTA_SECOND, JWT_ALOGITMA

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
        token_firebase_rw = request.json.get("token_firebase")
        print token_firebase_rw
                  

        # call method to encrypt password 
        pass_enc = encrypt(password_rw)
        
        #query login
        sql = t_user.query.filter_by(user_email=email_rw).filter_by(user_pw=pass_enc).all()

        print len(sql)

        if len(sql) > 0:
            # update token firebase
            sql_update = db.session.query(t_user).filter_by(user_email = email_rw).update({"token_firebase":token_firebase_rw})
            db.session.commit()

            sql1 = db.session.query(
                t_user.id,
                t_user.user_email,
                t_user.user_pw,
                t_user.user_nm,
                t_user.user_jk,
                t_user.user_notelp,
                t_user.user_birthDate,
                t_user.token_firebase
            ).filter_by(user_email = email_rw)

            data_user = s_user().dump(sql1, many=True).data
            
            #make new structure json
            data1 = []
            for i in range(len(data_user['data'])):
                userid = data_user['data'][i]['id']
                t_firebase = data_user['data'][i]['attributes']['token_firebase']
                names =data_user['data'][i]['attributes']['user_nm']

                data1.insert(i, {
                    'id'    :data_user['data'][i]['id'],
                    'email' :data_user['data'][i]['attributes']['user_email'],
                    'name'  :data_user['data'][i]['attributes']['user_nm'],
                    'jk'    :data_user['data'][i]['attributes']['user_jk'],
                    'notelp':data_user['data'][i]['attributes']['user_notelp'],
                    'token_firebase' :data_user['data'][i]['attributes']['token_firebase']
                })
            tokens=createToken(userid)
            #replace data_user become data_json
            data_user=data1
            message = "Apa kabarmu hari ini " + names + "?"
            # print names
            push_notification(t_firebase, message)

            resp = {'success' : 'true', 'msg': 'Login Success, Welcome.', 'data':data_user, 'token':tokens }, 200
            
            # sentEml= senEmail(email_rw)             #send parameter
            # sentEml.oto()                           #run the method
            
        else:
                #login failed
            resp = {'success' : 'false', 'msg': 'Login failed.' }
            
        
        return resp

def createToken(userId):
    payload = {
        'userid'    : userId,
        'exp'       : datetime.utcnow() + timedelta(weeks=JWT_EXP_DELTA_SECOND)
    }
    token = jwt.encode(payload, SECRET_KEY, JWT_ALOGITMA)
    token_decode = token.decode('utf-8')
    return token_decode

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
        token_rw = request.json.get("token_firebase")

        # print nama_rw, email_rw, password_rw, notelp_rw, jk_rw
        # encrypt password
        pass_enc = encrypt(password_rw)

        # print nama_rw, email_rw, password_rw, notelp_rw, jk_rw

        try:
            chekEmail = t_user.query.filter_by(user_email = email_rw).all()
            print len(chekEmail)
            if len(chekEmail) > 0 :
                resp = {'status':'false', 'msg':'Email sudah digunakan.'}
            else :
                lastid = db.session.query(func.max(t_user.id)).one()[0]
                if lastid == None: 
                    lastid = 0
                userid = int(lastid) + 1
                
                # if date == "00" and month == "00" and year == "0000" :
                #     date = "01"
                #     month = "01"
                #     year = "2000"
                
                # birthdate= year+'-'+month+'-'+date

                #insert data to db
                user = t_user(userid, email_rw, pass_enc, nama_rw, jk_rw, notelp_rw, token_rw)
                user.add(user)

                #get data from db
                getdata = db.session.query(
                    t_user.id,
                    t_user.user_nm,
                    t_user.user_email,
                    t_user.user_pw,
                    t_user.user_jk,
                    t_user.user_notelp,
                    t_user.token_firebase
                ).filter_by(id = userid)

                dataUser = s_user().dump(getdata, many = True).data
                
                #make new struktur json
                data1 = []
                for i in range(len(dataUser['data'])):
                    t_firebase = dataUser['data'][i]['attributes']['token_firebase']
                    names =dataUser['data'][i]['attributes']['user_nm']
                    data1.insert(i, {
                        'id':       dataUser['data'][i]['id'],
                        'name':     dataUser['data'][i]['attributes']['user_nm'],
                        'email':    dataUser['data'][i]['attributes']['user_email'],
                        'jk':       dataUser['data'][i]['attributes']['user_jk'],
                        'notelp':   dataUser['data'][i]['attributes']['user_notelp']
                    })
                #replace realdata to data1
                dataUser = data1
                tokens = createToken(userid)

                message ="Selamat bargabung di CAMART " + names
                push_notification(t_firebase, message)

                # send email otomatis
                # sentEml= senEmail(email_rw)             #send parameter
                # sentEml.oto()

                resp = {'status':'true', 'msg':'Selamat anda telah terdaftar.', 'data': dataUser, 'token':tokens}, 200
        
        except Exception as err:
            print err
            resp = {'status':'false', 'msg':'Gagal mendaftarkan data.'}, 401

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

class add_address(Resource):
    def post(self):
        raw_dict = request.json.get
        id_user = raw_dict("id_user")
        nm_penerima = raw_dict("nama")
        almt = raw_dict('alamat')
        province = raw_dict('provinsi')
        notelp = raw_dict('notelp')

        try:
            lastid = db.session.query(func.max(t_address.id)).one()[0]
            if lastid == None:
                lastid = 0
            id = int(lastid)+1
            print id, nm_penerima, almt, province, id_user
            sql = t_address(id, nm_penerima, almt, province, notelp, id_user)
            sql.add(sql)
            resp = {'success':'true', 'msg':'berhasil menambahkan alamat'}, 200
        except Exception as err:
            resp = {'success':'false','msg':'gagal menambahkan alamat'}, 400

        return resp

class updateUser(Resource):
    def post(self):

        req = request.json.get
        idUser_rw   = req("idUser")
        name_rw     = req("name")
        email_rw    = req("email")
        notelp_rw   = req("notelp")
        jk_rw       = req("jk")
        lastPw      = req("lastPassword")
        newPw       = req("newPassword")
        print idUser_rw, name_rw, email_rw, notelp_rw, jk_rw, lastPw, newPw

        lastPwEn = encrypt(lastPw)
        newPwEn   = encrypt(newPw)
        try:
            get_pw = db.session.query(t_user.user_pw).filter_by(id= idUser_rw).one()[0]
            print lastPwEn
            print get_pw
            if lastPwEn == get_pw:
                sql = db.session.query(t_user).filter_by(id = idUser_rw).update({
                    "user_email":email_rw, "user_pw":newPwEn, "user_nm":name_rw,"user_jk":jk_rw,
                     "user_notelp":notelp_rw})
                db.session.commit()

                t_firebase = db.session.query(t_user.token_firebase).filter_by(id= idUser_rw).one()[0]
                message = "Data kamu berhasil di perbaharui.."
                push_notification(t_firebase, message)

                resp = {"success":"true", "msg":"Data berhasil di perbaharui"}, 200
                
            else:
                resp ={"success":"false", "msg":"Password lama anda salah."}, 200

        except Exception as err:
            print err
            resp ={"success":"false", "msg":"gagal memperbaharui data"}, 200
        
        return resp

#url_prefix='/api/v1/users'
api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(address, '/address')
api.add_resource(add_address, '/new_address')
api.add_resource(updateUser, '/update')