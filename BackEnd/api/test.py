# this is a test file for testing/debugging analysis module
from model_driven_analysis import vulnerability_graph, ModelDriven_init, ModelDriven, centrality, origin_to_node_metrics, shortest_paths_gen,TOPSIS
import time
def network_topology_model_driven_input():
    # test file opening
    import json
    with open('./model.json') as f:
        network = json.load(f)

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

    TOPSIS()
    return 'Done', 21


network_topology_model_driven_input()

# import requests
# import json

# r = requests.get('http://127.0.0.1:2000/api/search/microsoft/xbox_360')
# print(json.loads(r.text)["results"])