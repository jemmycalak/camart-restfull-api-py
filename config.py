# DATABASE SETTINGS
pg_db_username = 'postgres'
pg_db_password = 'idg'
pg_db_name = 'camartdb'
pg_db_hostname = 'localhost'

#connect to db
DEBUG = True
PORT = 1401
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "camart_jemmycalak"
# PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                        DB_PASS=pg_db_password,
                                                                                        DB_ADDR=pg_db_hostname,
                                                                                        DB_NAME=pg_db_name)