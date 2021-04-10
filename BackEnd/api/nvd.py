
'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with local NVD. 

'''

from flask import Blueprint, jsonify, request
import requests
import json
import os
import numpy as np

httpHost    = "http://127.0.0.1:2000"       # ip and port of CVE Search
nvd_bp = Blueprint('nvd_bp', __name__)

@nvd_bp.route('/nvd/get_nvd_update_date', methods=['GET'])
def get_nvd_update_date():
    print(os.getcwd())
    with open('..\\dms\\cve_search\\log\\update_populate.log', 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
        return jsonify({"date" : last_line[:19]})

################# DATA DRIVEN QUERY ######################
# queries cvss score with CVE-Search
def data_driven_cvss_query(cve_id):
    global httpHost
    
    url = httpHost + "/api/cve/" + cve_id

    # making request to CVE ID
    r = requests.get(url)
    data = json.loads(r.text)

    cvss = np.array([0.0,0.0,0.0])

    # testing if cvss scores exist
    try:
        cvss[0] =  float(data["cvss"]) / 10.0
    except:
        cvss[0] = 1.0
    
    try:
        cvss[1] =  float(data["exploitabilityScore"]) / 10.0
    except:
        cvss[1] = 1.0
    
    try:
        cvss[2] =  float(data["impactScore"]) / 10.0
    except:
        cvss[2] = 1.0

    # base, exploitability, impact
    return cvss


############# MODEL DRIVEN QUERY ###################
def score_to_weight(score):
    if score >= 0.7:
        return 0.5
    elif score >= 0.4:
        return 0.3
    else:
        return 0.2

# queries cvss score with CVE-Search
def model_driven_cvss_query(cve_ids):
    global httpHost
    
    scores = np.array([0.0,0.0,0.0])
    weights = np.array([0.0,0.0,0.0])
    tmp = np.array([0.0,0.0,0.0])
    tmpW = np.array([0.0,0.0,0.0])
    for cve in cve_ids:
        url = httpHost + "/api/cve/" + cve

        # making request to CVE ID
        r = requests.get(url)
        data = json.loads(r.text)
        
        # testing if cvss scores exist
        try:
            tmp[0] =  float(data["cvss"]) / 10.0
        except:
            tmp[0] = 1
        
        try:
            tmp[1] =  float(data["exploitabilityScore"]) / 10.0
        except:
            tmp[1] = 1
        
        try:
            tmp[2] =  float(data["impactScore"]) / 10.0
        except:
            tmp[2] = 1

        tmpW[:] = [score_to_weight(tmp[0]), score_to_weight(tmp[1]), score_to_weight(tmp[2])]
        scores += tmp * tmpW
        weights += tmpW

    # calculating weighted average
    scores /= weights

    return scores

