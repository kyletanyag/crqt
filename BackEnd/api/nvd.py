
'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with local NVD. 

'''

from flask import Blueprint, jsonify, request
# from .data_models import NVD
import requests
import json
import os

httpHost    = "http://127.0.0.1:2000"       # ip and port of CVE Search
nvd_bp = Blueprint('nvd_bp', __name__)

@nvd_bp.route('nvd/get_nvd_update_date', methods=['GET'])
def get_nvd_update_date():
    with open('..\\dms\\cve_search\\log\\update_populate.log', 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
        return jsonify({"date" : last_line[:19]})

################# DATA DRIVEN QUERY ######################
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

