'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with local NVD. 

'''
from flask import Blueprint, jsonify, request
from . import db 

nvd_bp = Blueprint('nvd_bp', __name__)

# query with database to get cve_ids
def cvss_query(cve_ids):
    pass

# updates database with latest nvd
def update_nvd():
    pass