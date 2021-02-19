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
    username = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String (30))
    last_name = db.Column(db.String (30))
    email = db.Column(db.String (40), unique=True)
    user_role = db.Column(db.Integer, default=User_Role(0)) #Need to look up how to implement ENUM in Python/Flask. Roles = {Admin, User/Pleb}
    is_registered = db.Column(db.Boolean(), default=False) # Is this how to implement Boolean through Flask
    otp_secret = db.Column(db.String(16)) # Needs a Key.  What is contained in a key?  What is the object type 


# NVD Table
class NVD(db.Model):
    __bind_key__ = 'nvd'
    cve_id = db.Column(db.String(16), primary_key=True)
    base_score = db.Column(db.Float)
    exploitabiliy_score_v2 = db.Column(db.Float)
    impact_score_v2 = db.Column(db.Float)
    discription = db.Column(db.String(4000))