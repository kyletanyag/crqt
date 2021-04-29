# This file contains model- and data-driven examples

from graph_generation import network_topology_data_driven_input, network_topology_model_driven_input
import time
    


# contains examples for model-driven 
class model_driven_examples:   
    # makes weights equal to 1 / node id
    def custom_gen(json_file):
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
                cve_ids=None,
                product_type=""  
            ))
            vulnerability_graph[-1].weights[:] = 1.0 / float(node["id"])
            
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
    '''
    Calculates centrality metrics given network topology

    input is json file with model-driven network
    '''
    def centrality_example(json_file):
        from model_driven_analysis import betweenness_centrality, degree_centrality, closeness_centrality, katz_centrality, pagerank_centrality
        
        # generate weighted vulnerability graph
        network_topology_model_driven_input(json_file)

        degree = degree_centrality()        # indegree, outdegree, degree
        closeness = closeness_centrality()  # closeness
        between = betweenness_centrality()  # betweenness
        pagerank = pagerank_centrality()    # pagerank
        kc = katz_centrality()              # katz cen

        return degree, closeness, between, pagerank, kc

    '''
    Calculates attack path from remote attacker to node

    input is json file with model-driven network and node ID to compute attack paths for
    '''
    def attack_path_example(json_file, node_id):
        from model_driven_analysis import origin_to_node_metrics 

        # generate weighted vulnerability graph
        network_topology_model_driven_input(json_file)


        return origin_to_node_metrics(node_id)

    def layered_attack_analysis():
        from model_driven_analysis import origin_to_node_metrics, shortest_path_comp_time, shortest_paths_gen, vulnerability_graph, ModelDriven 
        

        switch = {
            ModelDriven.Layers.REMOTE_ATTACK    : "remote_attack", 
            ModelDriven.Layers.CORP_FW1         : "corp_fw_1",
            ModelDriven.Layers.CORP_DMZ         : "corp_dmz",
            ModelDriven.Layers.CORP_FW2         : "corp_fw_2",
            ModelDriven.Layers.CORP_LAN         : "corp_lan",
            ModelDriven.Layers.CS_FW1           : "cs_fw_1",
            ModelDriven.Layers.CS_DMZ           : "cs_dmz",
            ModelDriven.Layers.CS_FW2           : "cs_fw_2",
            ModelDriven.Layers.CS_LAN           : "cs_lan"
        }

        path = "./example/model_driven_input/"
        for json_file in ["load_test", "large_load_test"]:
            print(json_file)
            outfile = open(json_file + "_output_data.csv", "w")
            outfile.write(json_file + "\n")
            # generate weighted vulnerability graph
            model_driven_examples.custom_gen(path + json_file + ".json")

            # print("processing shortest path")
            # outfile.write("shortest_path_comp,")
            # shortest_paths_gen()
            # outfile.write(str(shortest_path_comp_time()) + "\n")

            for node in vulnerability_graph[1:]:
                if node.layer == ModelDriven.Layers.CS_LAN and (json_file != "load_test"):
                    break

                outfile.write(str(node.index) + ",")
                outfile.write(switch[node.layer] + ",")

                # tracemalloc.start()
                data = origin_to_node_metrics(node.index)
                t = data['computation_time']
                num_paths = data['number_attack_paths']
                # current, peak = tracemalloc.get_traced_memory()
                # tracemalloc.stop()

                outfile.write(str(num_paths) + "," + str(t) + "\n")
                print(node.index, ",", num_paths, ",", t)
            
            outfile.close()

    '''
    compute vulnerability host metrics

    input is json file with model-driven network
    '''
    def vulnerable_host_example(json_file):
        from model_driven_analysis import vulnerable_host_percentage

        # generate weighted vulnerability graph
        network_topology_model_driven_input(json_file)

        return vulnerable_host_percentage()

    '''
    compute TOPSIS metrics

    input is json file with model-driven network
    '''
    def topsis_example(json_file):
        from model_driven_analysis import TOPSIS

        # generate weighted vulnerability graph
        network_topology_model_driven_input(json_file)

        return TOPSIS()

# contains data-driven metric examples
class data_driven_examples:
    '''
    compute derived score metrics

    input is arcs and vertices csv files for LAG
    '''
    def derived_score_example(arcs_csv, vertices_csv):
        # generate weighted LAG and returns derived score metrics
        derived_scores = network_topology_data_driven_input(arcs_csv, vertices_csv)

        return derived_scores

    '''
    compute %execCode nodes

    input is arcs and vertices csv files for LAG
    '''
    def percentage_execCode_nodes_example(arcs_csv, vertices_csv):
        from data_driven_analysis import percentage_execCode_nodes

        # generate weighted LAG
        network_topology_data_driven_input(arcs_csv, vertices_csv)

        return percentage_execCode_nodes()    

    '''
    compute percentage rule nodes

    input is arcs and vertices csv files for LAG
    '''
    def percentage_rule_nodes_example(arcs_csv, vertices_csv):
        from data_driven_analysis import percentage_rule_nodes

        # generate weighted LAG
        network_topology_data_driven_input(arcs_csv, vertices_csv)

        return percentage_rule_nodes()   

    '''
    compute network_entropy

    input is arcs and vertices csv files for LAG
    '''
    def network_entropy_example(arcs_csv, vertices_csv):
        from data_driven_analysis import network_entropy

        # generate weighted LAG
        network_topology_data_driven_input(arcs_csv, vertices_csv)

        return network_entropy() 

if __name__ == "__main__":
    model_driven_examples.layered_attack_analysis()