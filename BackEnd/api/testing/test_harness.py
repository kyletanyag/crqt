# this is a test file for testing/debugging analysis module

# testing model 
import time
from collections import deque
import random as rng
import numpy as np

def model_driven_test():
    # test file opening
    from model_driven_analysis import vulnerability_graph, ModelDriven_init, ModelDriven, centrality, origin_to_node_metrics, shortest_paths_gen, TOPSIS
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


class data_driven_tests:
    ''' Testing derived score AND/rule node computation:
    It tests it by calculating rule node probability given n-nodes pointing at rule node.
    If test is succesful, the rule node should return product(n-node probabilities).

    The parameters for test is the number of nodes. Given that, a random probability will be assigned to each node
    '''
    def derived_score_AND_test(num_nodes, seed=50):
        # importing LAG to hold data and DerivedScore()
        from data_driven_analysis import LAG, DerivedScore, DataDriven

        # used by DerivedScore() to calculate derive scores
        leaf_queue = deque()

        # setting random seed
        np.random.seed(seed)

        # constructing leafs
        for i in range(num_nodes):
            LAG.append(DataDriven.Node(i, "LEAF", ""))
            LAG[i].node_type = DataDriven.Node_Type.PRIMITIVE_FACT

            # setting initial derived score for leaf node
            LAG[i].derived_score = np.random.rand(3)

            # pushing to queue
            leaf_queue.append(LAG[-1])
        
        LAG.append(DataDriven.Node(num_nodes,"AND", ""))
        LAG[-1].node_type = DataDriven.Node_Type.DERIVATION

        # setting all leafs nodes to point at RULE node
        for i in range(num_nodes):
            # setting leaf to point at RULE node
            LAG[i].next_node.append(LAG[-1])
            
            # telling RULE node how many nodes to process
            LAG[-1].calculations_remaining += 1
        
        # calculate derived score
        DerivedScore(leaf_queue)

        # re-import LAG
        from data_driven_analysis import LAG

        # calculate expected value
        print("expected:", np.prod([node.derived_score for node in LAG[:-1]], axis=0))

        print("output:",LAG[-1].derived_score)

    ''' Testing derived score OR/derived node computation:
    It tests it by calculating derived node probability given n-nodes pointing at derived node.
    If test is succesful, the derived node should return 1 - product(1 - n-node probabilities).

    The parameters for test is the number of nodes. Given that, a random probability will be assigned to each node
    '''
    def derived_score_OR_test(num_nodes, seed=50):
        # importing LAG to hold data and DerivedScore()
        from data_driven_analysis import LAG, DerivedScore, DataDriven

        # used by DerivedScore() to calculate derive scores
        leaf_queue = deque()

        # setting random seed
        np.random.seed(seed)

        # constructing leafs
        for i in range(num_nodes):
            LAG.append(DataDriven.Node(i, "LEAF", ""))
            LAG[i].node_type = DataDriven.Node_Type.PRIMITIVE_FACT

            # setting initial derived score for leaf node
            LAG[i].derived_score = np.random.rand(3)

            # pushing to queue
            leaf_queue.append(LAG[-1])
        
        LAG.append(DataDriven.Node(num_nodes,"OR", ""))
        LAG[-1].node_type = DataDriven.Node_Type.DERIVED

        # setting all leafs nodes to point at derived node
        for i in range(num_nodes):
            # setting leaf to point at derived node
            LAG[i].next_node.append(LAG[-1])
            
            # telling derived node how many nodes to process
            LAG[-1].calculations_remaining += 1
        
        # calculate derived score
        DerivedScore(leaf_queue)

        # re-import LAG
        from data_driven_analysis import LAG

        # calculate expected value
        print("expected:", 1 - np.prod([1 - node.derived_score for node in LAG[:-1]], axis=0))

        print("output:", LAG[-1].derived_score)

    ''' Testing derived score OR/derived node and AND/rule node computation to test propagation:
    It tests it by creating a multi-layer network where first layer contains leaf n-nodes, second layer
    contains 1-rule node, third layer contains n-rule nodes, and fourth layer contains 1-derived node.
    
    If test is succesful, second and third layer nodes should equal to product(first layer nodes) and 
    fourth layer should equal 1 - product(1-third layer nodes).

    The parameters for test is the number of leaf nodes and third layer rule nodes. 
    Given that, a random probability will be assigned to each node
    '''
    def derived_score_propagation_test(num_nodes, seed=50):
        # importing LAG to hold data and DerivedScore()
        from data_driven_analysis import LAG, DerivedScore, DataDriven

        # used by DerivedScore() to calculate derive scores
        leaf_queue = deque()

        # setting random seed
        np.random.seed(seed)

        # constructing leafs nodes (first layer)
        for i in range(num_nodes):
            ## leaf node
            LAG.append(DataDriven.Node(i, "LEAF", ""))
            LAG[-1].node_type = DataDriven.Node_Type.PRIMITIVE_FACT

            # setting initial derived score for leaf node
            LAG[-1].derived_score = np.random.rand(3)

            # pushing to queue
            leaf_queue.append(LAG[-1])

        # second layer
        LAG.append(DataDriven.Node(num_nodes,"AND", ""))
        LAG[-1].node_type = DataDriven.Node_Type.DERIVATION
        

        # third layer nodes
        for i in range(num_nodes):
            ## rule nodes
            LAG.append(DataDriven.Node(i, "AND", ""))
            LAG[-1].node_type = DataDriven.Node_Type.DERIVATION

        # fourth layer
        LAG.append(DataDriven.Node(num_nodes,"OR", ""))
        LAG[-1].node_type = DataDriven.Node_Type.DERIVED

        # setting all first layer to point at second layer
        for i in range(num_nodes):
            # setting leaf to point at derived node
            LAG[i].next_node.append(LAG[num_nodes])
            
            # telling derived node how many nodes to process
            LAG[num_nodes].calculations_remaining += 1
        
        # setting all second layer to point at third layer
        for i in range(num_nodes):
            # setting leaf to point at derived node
            LAG[num_nodes].next_node.append(LAG[num_nodes + i + 1])
            
            # telling derived node how many nodes to process
            LAG[num_nodes + i + 1].calculations_remaining += 1
        
        # setting all third layer to point at fourth layer
        for i in range(num_nodes):
            # setting leaf to point at derived node
            LAG[num_nodes + i + 1].next_node.append(LAG[-1])
            
            # telling derived node how many nodes to process
            LAG[-1].calculations_remaining += 1

        # calculate expected value
        second_layer = np.prod([node.derived_score for node in LAG[:num_nodes]], axis=0) 
        fourth_layer = 1 - np.power(1-second_layer,num_nodes)                   
        print("expected:", "2nd layer (rule node):", second_layer, "| fourth layer (derived node):", fourth_layer)

        # calculate derived score
        DerivedScore(leaf_queue)

        # re-import LAG
        from data_driven_analysis import LAG

        print("Output:", "2nd layer (rule node):", LAG[num_nodes].derived_score, "| fourth layer (derived node):", LAG[-1].derived_score)

# testing cve-search
def cve_search_test(cve_ids=[]):
    from nvd import data_driven_cvss_query

    # querying cve_ids then comparing with NVD online
    for cve_id in cve_ids:
        print(data_driven_cvss_query(cve_id))


if __name__ == "__main__":
    data_driven_tests.derived_score_propagation_test(4)