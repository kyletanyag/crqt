'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with local NVD. 

'''

from flask import Blueprint, jsonify, request
from .data_models import NVD

nvd_bp = Blueprint('nvd_bp', __name__)

# query with database to get cve_ids
@nvd_bp.route('/data_driven_cvss_query')
def data_driven_cvss_query(cve_id):
    nvd = NVD.query.get(cve_id)
    return [nvd.base_score, nvd.exploitabiliy_score_v2,nvd.impact_score_v2]


####### STILL IN WORK:

# @nvd_bp.route('/model_driven_cvss_query')
def model_driven_cvss_query(cve_ids):
    pass

# updates database with latest nvd
# @nvd_bp.route('/update_nvd')
# def update_nvd(cve_ids):
#     for data in nvd.query.filter(nvd["cve id"]).all():
#         if cve_ids not in data:
#             nvd.add(cve_ids)
#             nvd.commit()