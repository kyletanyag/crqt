'''
@author Thomas Laverghetta
@brief this file contains all the database models used by SQLAlchemy. 

'''
from . import db

class Users(db.Model):
    __bind_key__ = 'users'
    _username = db.Column(db.Integer, primary_key=True)
    _password = db.Column(db.Integer)

class NVD(db.Model):
    __bind_key__ = 'nvd'
    _cve_id = db.Column(db.String(16), primary_key=True)
    _base_score = db.Column(db.Float)
    _exploitabiliy_score_v2 = db.Column(db.Float)
    _impact_score_v2 = db.Column(db.Float)
    _discription = db.Column(db.String(120))
