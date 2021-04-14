'''
@author Thomas Laverghetta
@brief this file contains all the database models used by SQLAlchemy. 

'''
from . import db
import enum


# Enum for user roles
class User_Role(enum.Enum):
    ADMIN = 1
    GENERAL_USER = 0


# User table
class Users(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String (128), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    user_role = db.Column(db.Integer, default=User_Role(0))
    is_registered = db.Column(db.Boolean(), default=False) 
    otp_secret = db.Column(db.String(16)) # OTP KEY
    enabled_2fa = db.Column(db.Integer, default=False) 

# Products Table
class Products(db.Model):
    __bind_key__ = 'products'
    vendor = db.Column(db.String(64))
    type = db.Column(db.String(64))
    product = db.Column(db.String(64), primary_key=True)
