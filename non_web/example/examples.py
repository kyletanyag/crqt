# This file contains model- and data-driven examples

from non_web.graph_generation import network_topology_data_driven_input, network_topology_model_driven_input

# contains examples for model-driven 
class model_driven_examples:    
    '''
    Calculates centrality metrics given network topology

    input is json file with model-driven network
    '''
    def centrality_example(json_file):
        from non_web.model_driven_analysis import betweenness_centrality, degree_centrality, closeness_centrality, katz_centrality, pagerank_centrality
        
        # generate weighted vulnerability graph
        network_topology_data_driven_input(json_file)

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
        from non_web.model_driven_analysis import origin_to_node_metrics 

        # generate weighted vulnerability graph
        network_topology_data_driven_input(json_file)


        return origin_to_node_metrics(node_id)

    '''
    compute vulnerability host metrics

    input is json file with model-driven network
    '''
    def vulnerable_host_example(json_file):
        from non_web.model_driven_analysis import vulnerable_host_percentage

        # generate weighted vulnerability graph
        network_topology_data_driven_input(json_file)

        return vulnerable_host_percentage()

    '''
    compute TOPSIS metrics

    input is json file with model-driven network
    '''
    def topsis_example(json_file):
        from non_web.model_driven_analysis import TOPSIS

        # generate weighted vulnerability graph
        network_topology_data_driven_input(json_file)

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
        from non_web.data_driven_analysis import percentage_execCode_nodes

        # generate weighted LAG
        network_topology_data_driven_input(arcs_csv, vertices_csv)

        return percentage_execCode_nodes()    

    '''
    compute percentage rule nodes

    input is arcs and vertices csv files for LAG
    '''
    def percentage_rule_nodes_example(arcs_csv, vertices_csv):
        from non_web.data_driven_analysis import percentage_rule_nodes

        # generate weighted LAG
        network_topology_data_driven_input(arcs_csv, vertices_csv)

        return percentage_rule_nodes()   

    '''
    compute network_entropy

    input is arcs and vertices csv files for LAG
    '''
    def network_entropy_example(arcs_csv, vertices_csv):
        from non_web.data_driven_analysis import network_entropy

        # generate weighted LAG
        network_topology_data_driven_input(arcs_csv, vertices_csv)

        return network_entropy() 

if __name__ == "__main__":
    model_driven_examples.attack_path_example('./model_driven_input/model_driven1.json', 3)