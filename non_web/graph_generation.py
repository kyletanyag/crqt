'''
@author Thomas Laverghetta
@brief This is the logical attack graph (LAG) generation module. It will accept csv files from front-end which contain vertices and edges for user provided network. 

'''
from nvd import data_driven_cvss_query
from round_sig import round_sig
import time

# generates weighted LAG and calculates derived scores
# inputs: arcs and vertices csv files
def network_topology_data_driven_input(arcs_file, vertices_file, rule_probability=0.8):
    from data_driven_analysis import DataDriven, DerivedScore, DataDriven_init, LAG, LEAF_QUEUE
    import csv 

    # timing 
    start_timer = time.time()

    # initializing data-driven
    DataDriven_init()

    # opening vertices
    with open(vertices_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for node in reader:
            LAG.append(DataDriven.Node(int(node["id"]), node["logic"], node["description"]))

            # checking if derivation node
            if node["description"][:4] == 'RULE':
                LAG[-1].node_type = DataDriven.Node_Type.DERIVATION
                LAG[-1].derived_score[:] = rule_probability

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
                LEAF_QUEUE.append(LAG[-1])

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
    with open(arcs_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for edge in reader:
            targetNode = int(edge["nextNode"]) - 1
            LAG[int(edge["currNode"]) - 1].next_node.append(LAG[targetNode]) 
            LAG[targetNode].calculations_remaining += 1         # increase number of nodes needed for calculation

    parsing_time = time.time() - start_timer

    # calculates derived scores for all nodes
    return DerivedScore(LEAF_QUEUE)


# creates weighted vulnerability graph.
# input is json filename
def network_topology_model_driven_input(json_file):
    from model_driven_analysis import vulnerability_graph, ModelDriven, shortest_paths_gen, ModelDriven_init
    import json

    with open(json_file) as f:
        network = json.load(f)

    # initializing model-driven 
    ModelDriven_init() 

    # creating remote attacker node
    vulnerability_graph.append(ModelDriven.Node(None, None, "remote_attack", 0, None, None))
        
    for node in network["vertices"]:
        vulnerability_graph.append(ModelDriven.Node(
            product=node["product"], 
            vendor=node["vendor"],
            layer=node["layer"],
            index=node["id"],
            cve_ids=node["cve_ids"],
            product_type=node["type"]
        ))
        
    # sorting vulnerability node list by index ascending order
    vulnerability_graph.sort(key=lambda node: node.index)

    # edges
    for edges in network['arcs']:
        curr = edges["currNode"]
        for tar in edges["nextNode"]:
            ModelDriven.Edge(vulnerability_graph[curr], vulnerability_graph[tar])
            
    # connecting remote attacker
    for node in vulnerability_graph:
        if node.layer == ModelDriven.Layers.CORP_FW1:
            ModelDriven.Edge(vulnerability_graph[0], node)

    print("ready to calculate metrics")