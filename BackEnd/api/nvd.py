
'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with local NVD. 

'''

from flask import Blueprint, jsonify, request
# from .data_models import NVD
import requests
import json

httpHost    = "http://127.0.0.1:2000"       # ip and port of CVE Search
# nvd_bp = Blueprint('nvd_bp', __name__)

nvd_bp = Blueprint('nvd_bp', __name__)

# query with NVD database to get cve_ids
def data_driven_cvss_query(cve_id):
    global httpHost
    
    url = httpHost + "/api/cve/" + cve_id

    # making request to CVE ID
    r = requests.get(url)
    data = json.loads(r.text)
    
    scores = [0.0,0.0,0.0]       # base, exploitability, impact

    scores[0] = float(data["cvss"]) / 10.0
    
    scores[1] = float(data["exploitabilityScore"]) / 10.0

    scores[2] = float(data["impactScore"]) / 10.0

    return scores


############# MODEL DRIVEN QUERY ###################
def score_to_weight(score):
    if score >= 0.7:
        return 0.5
    elif score >= 0.4:
        return 0.3
    else:
        return 0.2

def model_driven_cvss_query(cve_ids):
    global httpHost
    weights = []
    scores = []
    
    for cve in cve_ids:
        url = httpHost + "/api/cve/" + cve

        # making request to CVE ID
        r = requests.get(url)
        data = json.loads(r.text)
        
        weights.append([0.0,0.0,0.0])
        scores.append([0.0,0.0,0.0])       # base, exploitability, impact

        scores[-1][0] = float(data["cvss"]) / 10.0
        weights[-1][0] = score_to_weight(scores[-1][0])

        scores[-1][1] = float(data["exploitabilityScore"]) / 10.0
        weights[-1][1] = score_to_weight(scores[-1][1])

        scores[-1][2] = float(data["impactScore"]) / 10.0
        weights[-1][2] = score_to_weight(scores[-1][2])
    
    result = [0.0,0.0,0.0]
    weight_sum = [0.0,0.0,0.0]
    # calculating weighted average
    for i in range(len(weights)):
        for j in range(3):
            result[j] += (scores[i][j] * weights[i][j])
            weight_sum[j] += weights[i][j]
    
    for i in range(3):
        result[i] = result[i] / weight_sum[i]

    return result
    
# # query with Products database to get vendor products by vendor name
# @nvd_bp.route('/product_query_by_vendor/', methods=['POST'])
# def query_by_vendor():
#     rq =  request.get_json() # vendor name
#     filter = Products.query.filter_by(vendor=rq['vendor'])
#     results = []

#     for i in filter:
#         results.append({
#             'vendor': results.vendor,
#             'type': results.type,
#             'product': results.product})

#     return jsonify({'Query': results})

# # query with Products database to get vendor products by product type
# @nvd_bp.route('/product_query_by_type/', methods=['POST'])
# def query_by_type():
#     rq =  request.get_json() # product type
#     filter = Products.query.filter_by(type=rq['type'])
#     results = []

#     for i in filter:
#         results.append({
#             'vendor': results.vendor,
#             'type': results.type,
#             'product': results.product})

#     return jsonify({'Query': results})

# # query with Products database to get vendor products by product name
# @nvd_bp.route('/product_query_by_name/', methods=['POST'])
# def query_by_product():
#     rq =  request.get_json() # product name
#     filter = Products.query.filter_by(product=rq['product'])
#     results = []

#     for i in filter:
#         if i.product == True:   
#             results.append({
#                 'vendor': results.vendor,
#                 'type': results.type,
#                 'product': results.product})

#     return jsonify({'Query': results})

####### STILL IN WORK:

# updates database with latest nvd
# @nvd_bp.route('/update_nvd')
# def update_nvd(cve_ids):
#     for data in nvd.query.filter(nvd["cve id"]).all():
#         if cve_ids not in data:
#             nvd.add(cve_ids)
#             nvd.commit()


