import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/idea-bbdd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'una_clave_secreta_segura'  # Necesario para WTForms