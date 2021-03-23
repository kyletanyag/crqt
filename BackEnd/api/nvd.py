'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with local NVD. 

'''

from flask import Blueprint, jsonify, request
from .data_models import NVD


nvd_bp = Blueprint('nvd_bp', __name__)

# query with database to get cve_ids
def data_driven_cvss_query(cve_id):
    nvd = NVD.query.get(cve_id)
    return [nvd.base_score/10.0, nvd.exploitabiliy_score_v2/10.0,nvd.impact_score_v2/10.0]

@nvd_bp.route('/cvss_query', methods=['POST'])
def cvss_query():
    cve_id = request.get_json()  # json network topology data driven
    print(cve_id['cve'])
    nvd = NVD.query.get(cve_id['cve'])
    return jsonify({
        'base': nvd.base_score, 
        'exploitability' : nvd.exploitabiliy_score_v2,
        'impact' : nvd.impact_score_v2})

####### STILL IN WORK:

# updates database with latest nvd
# @nvd_bp.route('/update_nvd')
# def update_nvd(cve_ids):
#     for data in nvd.query.filter(nvd["cve id"]).all():
#         if cve_ids not in data:
#             nvd.add(cve_ids)
#             nvd.commit()



