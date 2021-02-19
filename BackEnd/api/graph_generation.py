'''
@author Thomas Laverghetta
@brief This is the logical attack graph (LAG) generation module. It will accept csv files from front-end which contain vertices and edges for user provided network. 

'''
from flask import Blueprint, jsonify, request
from .nvd import data_driven_cvss_query, CVSS, model_driven_cvss_query
import enum

# route for LAG generation module
graph_bp = Blueprint('graph_bp', __name__)

# Enum for node relationships
class Node_Logic(enum.Enum):
    AND = 0
    OR = 1
    FLOW = 2

# Enum for Node Types
class Node_Type(enum.Enum):
    PRIMITIVE_FACT = 0
    DERIVATION = 1
    DERIVED = 2

# graph data structure (adjenency list)
class Node:
    index = int()                   # node index
    cve_id = None                   # cve_id(s) optional
    cvss_score = CVSS()             # base, impact, exploitability score
    node_type = Node_Type(0)         # type of node // need to fix -- kbt 
    node_logic = Node_Logic(0)       # node relationship // need to fix -- kbt
    next_node = []                  # next nodes

@graph_bp.route('/network_topology_data_driven_input', methods=['POST'])
def network_topology_data_driven_input():
    network = request.get_json()  # json network topology data driven
    
    lag = []
    
    # vertices
    for node in network["vertices"]:
        lag.append(Node())
        lag[-1].index = int(node["id"])

        # searching for CVE ID
        cve_index = node["description"].find('CVE')
        if cve_index != -1: 
            # cve_id found
            pass
        
        lag[-1].node_logic = None


