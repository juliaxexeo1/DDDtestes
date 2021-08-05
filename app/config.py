#from app.sensive import Sensive as sensive f
import os
from os import environ

class Config:
    #SQLALCHEMY_DATABASE_URI=environ.get("DATABASE_URI")
    SQLALCHEMY_DATABASE_URI='postgresql://cyuokggaizepit:3326215bfcce9c5413e3a28f36e134de8a0b0d45a5331735aa0d59b6d282faeb@ec2-44-196-250-191.compute-1.amazonaws.com:5432/d9ltp43nbshbq9'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    SECRET_KET=environ.get('SECRET_KEY')