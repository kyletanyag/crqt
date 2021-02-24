'''
@author Thomas Laverghetta
@brief This is the logical attack graph (LAG) generation module. It will accept csv files from front-end which contain vertices and edges for user provided network. 

'''
from flask import Blueprint, jsonify, request
from .nvd import data_driven_cvss_query, model_driven_cvss_query
import enum
from collections import deque
from .analysis import Node, Node_Logic, Node_Type, PrimitiveFactNode, DerivedScore

# route for LAG generation module
graph_bp = Blueprint('graph_bp', __name__)

@graph_bp.route('/network_topology_data_driven_input', methods=['POST'])
def network_topology_data_driven_input():
    network = request.get_json()  # json network topology data driven
    
    lag = {}

    # vertices
    for node in network["vertices"]:
        lag[node["id"]] = Node()

        # setting logic
        if node["logic"] == "FLOW":
            lag[node["id"]].node_logic = Node_Logic.FLOW 
        elif node["logic"] == "AND":
            lag[node["id"]].node_logic = Node_Logic.AND
        elif node["logic"] == "OR":
            lag[node["id"]].node_logic = Node_Logic.OR
        else:
            lag[node["id"]].node_logic = Node_Logic.LEAF

        # checking if derivation node
        if node["description"][:3] == 'RULE':
            lag[node["id"]].node_type = Node_Type.DERIVATION

        # checking if primitive fact node (primitive fact nodes are always leafs)
        elif lag[node["id"]].node_logic == Node_Logic.LEAF: 
            lag[node["id"]].node_type = Node_Type.PRIMITIVE_FACT

        # else, derived fact node
        else:
            lag[node["id"]].node_type = Node_Type.DERIVED
        
    # edges
    for edge in network["arcs"]:
        lag[edge["currNode"]].next_node.append(edge["nextNode"]) 

    # constructing queue for leaf nodes for derived score calculations
    leaf_queue = deque()
    for key in lag:
        if lag[key].node_type == Node_Type.PRIMITIVE_FACT:
            tmp_node = PrimitiveFactNode()
            tmp_node.index = key
            tmp_node.next_node = lag[key].next_node

            # searching for CVE ID
            cve_index = node["description"].find('CVE')
            if cve_index != -1:
                # getting CVSS scores
                tmp_node.cvss_score = data_driven_cvss_query(node["description"][cve_index:(cve_index+13)])
            # else use default values (1.0)
            leaf_queue.append(tmp_node)

    DerivedScore(lag, leaf_queue)
        

@graph_bp.route('/network_topology_model_driven_input', methods=['POST'])
def network_topology_model_driven_input():
    pass