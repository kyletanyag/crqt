'''
@author Thomas Laverghetta
@brief This is the logical attack graph (LAG) generation module. It will accept csv files from front-end which contain vertices and edges for user provided network. 

'''
from flask import Blueprint, jsonify, request
from .nvd import data_driven_cvss_query
import enum
from collections import deque
from .data_driven_analysis import DataDriven, DerivedScore, DataDriven_init
from .model_driven_analysis import vulnerability_graph, ModelDriven, shortest_paths_gen, ModelDriven_init
import time

# input variables
title = ""                      # title/name of network
input_date = ""                 # date/time of network input into system

# route for LAG generation module
graph_bp = Blueprint('graph_bp', __name__)

@graph_bp.route('/get_network_title', methods=['GET'])
def get_network_title():
    return jsonify({"network_title" : title})

@graph_bp.route('/get_input_date', methods=['GET'])
def get_input_date():
    return jsonify({"input_date" : input_date})

@graph_bp.route('/network_topology_data_driven_input', methods=['POST'])
def network_topology_data_driven_input():
    network = request.get_json()  # json network topology data driven

    # timing 
    start_timer = time.time()

    # initializing data-driven
    DataDriven_init()
    
    # setting title and input date
    title = network["network_title"]
    input_date = network["date"]

    lag = {}

    # vertices
    for node in network["vertices"]:
        node_id = int(node["id"])
        lag[node_id] = DataDriven.Node()

        lag[node_id].description = node["description"]

        # setting logic
        if node["logic"] == "FLOW":
            lag[node_id].node_logic = DataDriven.Node_Logic.FLOW 
        elif node["logic"] == "AND":
            lag[node_id].node_logic = DataDriven.Node_Logic.AND
        elif node["logic"] == "OR":
            lag[node_id].node_logic = DataDriven.Node_Logic.OR
        else:
            lag[node_id].node_logic = DataDriven.Node_Logic.LEAF

        # checking if derivation node
        if node["description"][:4] == 'RULE':
            lag[node_id].node_type = DataDriven.Node_Type.DERIVATION
            for score in lag[node_id].derived_score:
                score = network["sim_config"]

        # checking if primitive fact node (primitive fact nodes are always leafs)
        elif lag[node_id].node_logic == DataDriven.Node_Logic.LEAF: 
            lag[node_id].node_type = DataDriven.Node_Type.PRIMITIVE_FACT

        # else, derived fact node
        else:
            lag[node_id].node_type = DataDriven.Node_Type.DERIVED
        
        # checking if node is execCode
        if lag[node_id].node_type == DataDriven.Node_Type.DERIVED:
            execCode_index = node["description"].find('execCode')
            if execCode_index != -1:
                # if execCode node, flag
                lag[node_id].isExecCode = True

    # edges
    for edge in network["arcs"]:
        targetNode = int(edge["nextNode"])
        lag[int(edge["currNode"])].next_node.append(targetNode) 
        lag[targetNode].calculations_remaining += 1              # increase number of nodes needed for calculation

    # constructing queue for leaf nodes for derived score calculations
    leaf_queue = deque()
    for key in lag:
        if lag[key].node_type == DataDriven.Node_Type.PRIMITIVE_FACT:
            # searching for CVE ID
            cve_index = lag[key].description.find('CVE')
            if cve_index != -1:
                end_position = lag[key].description.find('\'', cve_index)
                cve_id = lag[key].description[cve_index:end_position]

                # getting CVSS scores
                lag[key].derived_score = data_driven_cvss_query(cve_id)
                # print(cve_id, lag[key].derived_score)

            # else use default values (1.0)
            leaf_queue.append(lag[key])
        
        # print(key, lag[key].isExecCode)
    
    parsing_time = time.time() - start_timer

    DerivedScore(lag, leaf_queue)

    return "Done", parsing_time

        

@graph_bp.route('/network_topology_model_driven_input', methods=['POST'])
def network_topology_model_driven_input():
    network = request.get_json()  # json network topology data driven

    # setting title and input date
    title = network["network_title"]
    input_date = network["date"]

    # initializing model-driven 
    ModelDriven_init() 

    # creating remote attacker node
    vulnerability_graph.append(ModelDriven.Node(None, None, "remote_attack", 0))

    for node in network["vertices"]:
        vulnerability_graph.append(ModelDriven.Node(
            product=node["product"], 
            vendor=node["vendor"],
            layer=node["layer"],
            index=int(node["id"]),
            cve_ids=node["cve_ids"]
            ))

    # sorting vulnerability node list by index ascending order
    vulnerability_graph.sort(key=lambda node: node.index)

    # edges
    for edges in network['arcs']:
        ModelDriven.Edge(vulnerability_graph[int(edges["currNode"])], vulnerability_graph[int(edges["nextNode"])])


    # start generating shorest paths
    shortest_paths_gen()
    return 'Done', 21