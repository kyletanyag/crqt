'''
@author Thomas Laverghetta
@brief this file contains all the database models used by SQLAlchemy. 

'''
from . import db

class Users(db.Model):
    __bind_key__ = 'users'
    _username = db.Column("username", db.Integer, primary_key=True)
    _password = db.Column("passwd", db.Integer)

class NVD(db.Model):
    __bind_key__ = 'nvd'
    _cve_id = db.Column("cve_id", db.String(16), primary_key=True)
    _base_score = db.Column("base_score", db.Float)
    _exploitabiliy_score = db.Column("exploitabiliy_score_v2", db.Float)
    _impact_score = db.Column("impact_score_v2", db.Float)
    _discription = db.Column("discription",db.String(120))
