'''
@author Thomas Laverghetta
@brief This is the logical attack graph (LAG) generation module. It will accept csv files from front-end which contain vertices and edges for user provided network. 

'''
from flask import Blueprint, jsonify, request
from .nvd import data_driven_cvss_query
import enum
from collections import deque
from .data_driven_analysis import DataDriven, DerivedScore, DataDriven_init
from .model_driven_analysis import ModelDriven, shortest_paths_gen, ModelDriven_init
from .round_sig import round_sig
import time

# load percentage - percentage of loading file
load_percentage = 0.0

# input variables
title_data_driven = ""                      # title/name of network
input_date_data_driven = ""                 # date/time of network input into system

# route for LAG generation module
graph_bp = Blueprint('graph_bp', __name__)

@graph_bp.route('/file_load_percentage', methods=['GET'])
def file_load_percentage():
    global load_percentage
    return {"file_load_percentage" : round_sig(load_percentage*100.0,4)}

@graph_bp.route('/test_connection', methods=['GET'])
def test_connection():
    return 'Good Connection', 200

@graph_bp.route('/data_driven/get_network_title', methods=['GET'])
def data_get_network_title():
    global title_data_driven
    return jsonify({"network_title" : title_data_driven})

@graph_bp.route('/data_driven/get_input_date', methods=['GET'])
def data_get_input_date():
    global input_date_data_driven
    return jsonify({"input_date" : input_date_data_driven})

@graph_bp.route('/network_topology_data_driven_input', methods=['POST'])
def network_topology_data_driven_input():
    global title_data_driven
    global input_date_data_driven 
    global load_percentage
    from .data_driven_analysis import LAG

    load_percentage = 0.0

    network = request.get_json()  # json network topology data driven

    # timing 
    start_timer = time.time()

    # initializing data-driven
    DataDriven_init()
    
    # setting title and input date
    title_data_driven = network["network_title"]
    input_date_data_driven = network["date"]

    leaf_queue = deque()

    # vertices
    for node in network["vertices"]:
        LAG.append(DataDriven.Node(int(node["id"]), node["logic"], node["description"]))

        # checking if derivation node
        if node["description"][:4] == 'RULE':
            LAG[-1].node_type = DataDriven.Node_Type.DERIVATION
            LAG[-1].derived_score[:] = network["sim_config"]

        # checking if primitive fact node (primitive fact nodes are always leafs)
        elif LAG[-1].node_logic == DataDriven.Node_Logic.LEAF: 
            LAG[-1].node_type = DataDriven.Node_Type.PRIMITIVE_FACT

            # searching for CVE ID
            cve_index = LAG[-1].description.find('CVE')
            if cve_index != -1:
                end_position = LAG[-1].description.find('\'', cve_index)
                cve_id = LAG[-1].description[cve_index:end_position]

                # getting CVSS scores
                LAG[-1].derived_score = data_driven_cvss_query(cve_id)
                # print(cve_id, LAG[key].derived_score)

            # else use default values (1.0)
            leaf_queue.append(LAG[-1])

        # else, derived fact node
        else:
            LAG[-1].node_type = DataDriven.Node_Type.DERIVED
            
            # checking if node is execCode
            execCode_index = node["description"].find('execCode')
            if execCode_index != -1:
                # if execCode node, flag
                LAG[-1].isExecCode = True

        # calculating load percentage
        load_percentage += 0.5 / len(network["vertices"]) - 0.1       

    # sorting LAG by id
    LAG.sort(key=lambda node: node.index)

    # edges
    for edge in network["arcs"]:
        targetNode = int(edge["nextNode"]) - 1
        LAG[int(edge["currNode"]) - 1].next_node.append(LAG[targetNode]) 
        LAG[targetNode].calculations_remaining += 1         # increase number of nodes needed for calculation
    
    load_percentage = 0.9

    parsing_time = time.time() - start_timer

    # calculates derived scores for all nodes
    DerivedScore(leaf_queue)

    load_percentage = 1.0

    return {'parsing_time': round(parsing_time,4)}, 200



title_model_driven = ""                      # title/name of network
input_date_model_driven = ""                 # date/time of network input into system

@graph_bp.route('/model_drivenn/get_network_title', methods=['GET'])
def model_get_network_title():
    global title_model_driven
    return jsonify({"network_title" : title_model_driven})

@graph_bp.route('/model_driven/get_input_date', methods=['GET'])
def model_get_input_date():
    global input_date_model_driven
    return jsonify({"input_date" : input_date_model_driven})  

@graph_bp.route('/network_topology_model_driven_input', methods=['POST'])
def network_topology_model_driven_input():
    global title_model_driven
    global input_date_model_driven 
    global load_percentage
    from .model_driven_analysis import vulnerability_graph

    network = request.get_json()  # json network topology data driven

    # setting title and input date
    title_model_driven = network["network_title"]
    input_date_model_driven = network["date"]

    # initializing model-driven 
    ModelDriven_init() 

    # creating remote attacker node
    vulnerability_graph.append(ModelDriven.Node(None, None, "remote_attack", 0, None, None))
    
    load_percentage = 0.0
    
    for node in network["vertices"]:
        vulnerability_graph.append(ModelDriven.Node(
            product=node["product"], 
            vendor=node["vendor"],
            layer=node["layer"],
            index=node["id"],
            cve_ids=node["cve_ids"],
            product_type=node["type"]
            ))
        
        # calculating load percentage
        load_percentage += 0.5 / len(network["vertices"]) - 0.1

    # sorting vulnerability node list by index ascending order
    vulnerability_graph.sort(key=lambda node: node.index)

    # edges
    for edges in network['arcs']:
        curr = edges["currNode"]
        for tar in edges["nextNode"]:
            ModelDriven.Edge(vulnerability_graph[curr], vulnerability_graph[tar])
        
        load_percentage += 0.5 / len(network["vertices"]) - 0.1
    
    # connecting remote attacker
    for node in vulnerability_graph:
        if node.layer == ModelDriven.Layers.CORP_FW1:
            ModelDriven.Edge(vulnerability_graph[0], node)
    
    load_percentage += 0.5 / len(network["vertices"]) - 0.1

    # start generating shorest paths
    shortest_paths_gen()

    load_percentage = 1.0
    return 'Done', 201