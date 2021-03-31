# this is a test file for testing/debugging analysis module
from model_driven_analysis import vulnerability_graph, ModelDriven_init, ModelDriven, centrality, TOPSIS

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
            index=int(node["id"]),
            cve_ids=node["cve_ids"]
            ))

    # sorting vulnerability node list by index ascending order
    vulnerability_graph.sort(key=lambda node: node.index)

    # edges
    for edges in network['arcs']:
        ModelDriven.Edge(vulnerability_graph[int(edges["currNode"])], vulnerability_graph[int(edges["nextNode"])])


    # start generating shorest paths
    centrality()
    TOPSIS()
    return 'Done', 21


network_topology_model_driven_input()

# import requests
# import json

# r = requests.get('http://127.0.0.1:2000/api/search/microsoft/xbox_360')
# print(json.loads(r.text)["results"])