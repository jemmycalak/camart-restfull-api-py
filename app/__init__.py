from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MyResponse(Response):
    default_mimetype = 'application/xml'

class CRUD():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.response_class = MyResponse

    from app import db               #harus ada ini untuk buat table
    db.init_app(app)

    #Blueprints
    from app.views.v_users import users                 #import user di ambil dari blueprint v_user -> users=Blueprint('users', __name__)
    app.register_blueprint(users, url_prefix='/api/v1/users')

    from app.views.v_products import products            #import user di ambil dari blueprint v_user ->products=Blueprint('products', __name__)
    app.register_blueprint(products, url_prefix='/api/v1/products')

    from app.views.v_bank import banks
    app.register_blueprint(banks, url_prefix='/api/v1/banks')

    return app 

