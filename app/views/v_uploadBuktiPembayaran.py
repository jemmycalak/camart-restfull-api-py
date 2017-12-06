import cv2, os
from flask import Blueprint, request
from app import db
from flask_restful import Api, Resource
from sqlalchemy import func, sql, update, join
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import ValidationError
from app.models.m_buktiPembayaran import t_buktiPembayaran, s_buktiPembayaran
import base64, json
from PIL import Image
from base64 import decodestring
from datetime import date, datetime
import uuid

uploads = Blueprint('upload', __name__)

api = Api(uploads)


class uploadPembayaran(Resource):
    def post(self):
        
        file_rw = request.json.get("image")
        id_user_rw = request.json.get("id_user")
        id_order_rw = request.json.get("id_order")
        print id_user_rw, id_order_rw

        try:
        
            image_path = os.path.join('C:/xampp/htdocs/db_m_market_localhost/images/upload/')
            image_path_toDB = "http://192.168.43.66/db_m_market_localhost/images/upload/"
            
            if not os.path.isdir(image_path):
                os.mkdir(image_path)

            image_name = "images_"+str(uuid.uuid4())+".JPG"
            print image_name
            # decode image
            imageDecode = base64.b64decode(file_rw)
            with open(image_path + image_name, 'wb') as f:
                f.write(imageDecode)
                print f

            # insert to database
            lastidimage = db.session.query(func.max(t_buktiPembayaran.id)).one()[0]
            if lastidimage == None:
                lastidimage = 0
            
            print lastidimage

            id_image = int(lastidimage)+1
            insertImage = t_buktiPembayaran(id_image, id_order_rw, image_path_toDB+image_name)
            insertImage.add(insertImage)
            
            resp ={"status":"true", "msg":"berhasil menguplaod gambar"}, 200
        except Exception as err:
            print "error upload"
            resp = {"status":"false", "msg":"gagal mengupload gambar"}, 400

        return resp

def randomName():
    dateString = str(datetime.now())

    print dateString
    return dateString

# /api/v1/uploadBuktiPembayaran
api.add_resource(uploadPembayaran, '')
