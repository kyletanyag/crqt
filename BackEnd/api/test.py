from model_driven_analysis import vulnerability_graph, ModelDriven, shortest_paths_gen, katz_centrality_and_pagerank_centrality

def network_topology_model_driven_input():
    # test file opening
    import json
    with open('./model.json') as f:
        network = json.load(f)

    # creating remote attacker node
    vulnerability_graph.append(ModelDriven.Node(None, None, "remote_attack", 0))

    for node in network["vertices"]:
        vulnerability_graph.append(ModelDriven.Node(
            product=node["product"], 
            vendor=node["vendor"],
            layer=node["layer"],
            index=int(node["id"])
            ))

    # sorting vulnerability node list by index ascending order
    vulnerability_graph.sort(key=lambda node: node.index)

    # edges
    for edges in network['arcs']:
        ModelDriven.Edge(vulnerability_graph[int(edges["currNode"])], vulnerability_graph[int(edges["nextNode"])])


    # start generating shorest paths
    shortest_paths_gen()
    katz_centrality_and_pagerank_centrality()
    

    return {'Done': '21'}


network_topology_model_driven_input()