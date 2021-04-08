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
import time

# input variables
title = ""                      # title/name of network
input_date = ""                 # date/time of network input into system

# route for LAG generation module
graph_bp = Blueprint('graph_bp', __name__)

@graph_bp.route('/test_connection', methods=['GET'])
def test_connection():
    return 'Good Connection', 200

@graph_bp.route('/get_network_title', methods=['GET'])
def get_network_title():
    global title
    return jsonify({"network_title" : title})

@graph_bp.route('/get_input_date', methods=['GET'])
def get_input_date():
    global input_date
    return jsonify({"input_date" : input_date})

@graph_bp.route('/network_topology_data_driven_input', methods=['POST'])
def network_topology_data_driven_input():
    global title
    global input_date 
    from .data_driven_analysis import LAG

    network = request.get_json()  # json network topology data driven

    # timing 
    start_timer = time.time()

    # initializing data-driven
    DataDriven_init()
    
    # setting title and input date
    title = network["network_title"]
    input_date = network["date"]

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

    # sorting LAG by id
    LAG.sort(key=lambda node: node.index)

    # edges
    for edge in network["arcs"]:
        targetNode = int(edge["nextNode"]) - 1
        LAG[int(edge["currNode"]) - 1].next_node.append(LAG[targetNode]) 
        LAG[targetNode].calculations_remaining += 1         # increase number of nodes needed for calculation
        LAG[targetNode].diNumConditions += 1                # counting the number of conditions
    
    parsing_time = time.time() - start_timer

    # calculates derived scores for all nodes
    DerivedScore(leaf_queue)

    return {'parsing_time': parsing_time}, 200

        

@graph_bp.route('/network_topology_model_driven_input', methods=['POST'])
def network_topology_model_driven_input():
    global title
    global input_date 
    from .model_driven_analysis import vulnerability_graph

    network = request.get_json()  # json network topology data driven

    # setting title and input date
    title = network["network_title"]
    input_date = network["date"]

    # initializing model-driven 
    ModelDriven_init() 

    # creating remote attacker node
    vulnerability_graph.append(ModelDriven.Node(None, None, "remote_attack", 0, None))

    for node in network["vertices"]:
        vulnerability_graph.append(ModelDriven.Node(
            product=node["product"], 
            vendor=node["vendor"],
            layer=node["layer"],
            index=node["id"],
            cve_ids=node["cve_ids"]
            ))

    # sorting vulnerability node list by index ascending order
    vulnerability_graph.sort(key=lambda node: node.index)

    # edges
    for edges in network['arcs']:
        curr = edges["currNode"]
        for tar in edges["nextNode"]:
            ModelDriven.Edge(vulnerability_graph[curr], vulnerability_graph[tar])


    # start generating shorest paths
    shortest_paths_gen()
    return 'Done', 201