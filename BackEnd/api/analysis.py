from flask import Blueprint, jsonify, request
from enum import Enum, auto
from copy import deepcopy 
from collections import deque
from . import db 
import math
import scipy.linalg as la
import numpy as np

# route for LAG generation module
analysis_bp = Blueprint('analysis_bp', __name__)

# namespace for data-driven objects
class DataDriven:
    # Enum for node relationships
    class Node_Logic(Enum):
        AND = 0
        OR = 1
        FLOW = 2
        LEAF = 3

    # Enum for Node Types
    class Node_Type(Enum):
        PRIMITIVE_FACT = 0
        DERIVATION = 1
        DERIVED = 2

    # graph data structure (adjenency list) for DataDriven
    class Node:
        def __init__(self):
            self.derived_score = [1.0,1.0,1.0]   # base, exploitability, impact scores
            self.discription = str()             # node discription
            self.node_type = None                # type of node  
            self.node_logic = None               # node relationship 
            self.next_node = []                  # next nodes
            self.calculations_remaining = 0      # number of nodes needed to calculate derived score
            self.isExecCode = False              # whether node is execCode node (used for percentage execCode metric)

        def printFunc(self):
            print(self.derived_score, self.discription, self.node_type, self.node_logic, self.next_node, self.calculations_remaining, self.isExecCode)


'''
Probability Formulas:
For any n events e1, e2, ..., en:
	1. P(e1, e2, ..., en)=product(P(ei),1,n)				    // product (expression, lower, upper)
	2. P(e1 U e2 U ... U en) = 1 - product(P(NOT(ei)),1,n)		// http://people.duke.edu/~hpgavin/cee201/ProbabilityRules.pdf
'''
LAG = {}
# scores is derived scores tuple
# key is dictionary key to access node
def Depth_First_Alg(scores, key): 
    global LAG

    # reduce number of nodes needed to make calculation
    LAG[key].calculations_remaining -= 1

    # modifying score
    if LAG[key].node_logic == DataDriven.Node_Logic.OR:
        # OR = (1-p1)*...*(1-pn)
        for i in range(3):
            LAG[key].derived_score[i] = LAG[key].derived_score[i]*(1-scores[i])     # probability formula 2
    else: # node_log == AND OR FLOW
        # AND = p1*...*pn
        for i in range(3):
            LAG[key].derived_score[i] = LAG[key].derived_score[i]*scores[i]         # probability formula 1
    
    # if no more nodes are required to make calculation
    if LAG[key].calculations_remaining == 0:
        # if OR node, then finalize calculation
        # 1 - (1-p1)*...*(1-pn)
        if LAG[key].node_logic == DataDriven.Node_Logic.OR:
            for i in range(3):
                LAG[key].derived_score[i] = 1-LAG[key].derived_score[i]             # probability formula 2

        # next node(s)
        for k in LAG[key].next_node:
            Depth_First_Alg(LAG[key].derived_score, k)
    


def DerivedScore(lag_dict, leaf_queue):
    global LAG
    LAG = lag_dict
    
    # modifying derived scores
    while len(leaf_queue) > 0:
        node = leaf_queue.pop()
        for key in node.next_node:
            Depth_First_Alg(node.derived_score, key)
               
    # return LAG

@analysis_bp.route('/getDerivedScores', methods=['GET'])
def getDerivedScores():
    global LAG

    # converting to JSON
    node_type_to_str = {
        DataDriven.Node_Type.DERIVATION : 'Derivation', 
        DataDriven.Node_Type.DERIVED : 'Derived Fact',
        DataDriven.Node_Type.PRIMITIVE_FACT: 'Primitive Fact'}

    vertices = []
    edges = []
    for key in LAG: 
        vertices.append({
                'id' : key,
                'discription' : LAG[key].discription,
                'node_type' : node_type_to_str[LAG[key].node_type], 
                'base_score' : round(LAG[key].derived_score[0],3),
                'exploitability_score' : round(LAG[key].derived_score[1],3),
                'impact_score' : round(LAG[key].derived_score[2],3)})
        for e in LAG[key].next_node:
            edges.append({'source' : key, 'target' : e})
    
    return jsonify({'nodes': vertices, 'edges' : edges})

@analysis_bp.route('/test-derived-scores', methods=['GET'])
def test_Derived_Scores():
    nodes = [{
            'id': 1,
            'description': 'Something!',
            'node_type' : 'Leaf',
            'base_score' : 10,
            'exploitability_score': 5,
            'impact_score': 7
        },
        {
            'id': 2,
            'description': 'Something Part 2!',
            'node_type' : 'Leaf',
            'base_score' : 8,
            'exploitability_score': 4,
            'impact_score': 3
        }
    ]

    links = [{
            'source': '1',
            'target': '2'
        }
    ]

    return jsonify({'nodes': nodes, 'edges': links}), 200
#################### DATA-DRIVEN LAG Metrics ########################
@analysis_bp.route('/percentage_execCode_nodes', methods=['GET'])
def percentage_execCode_nodes():
    global LAG
    sum = 0
    for key in LAG:
        sum += LAG[key].isExecCode

    result=round((float(sum) / float(len(LAG)) * 100.0),3)
    print(sum)
    return jsonify({'percentage_execCode_nodes': result})


@analysis_bp.route('/percentage_rule_nodes', methods=['GET'])
def percentage_rule_nodes():
    global LAG
    rules = 0
    for key in LAG:
        rules += (LAG[key].node_type == DataDriven.Node_Type.DERIVATION)

    result=round((float(rules) / float(len(LAG)) * 100.0),3)
    return jsonify({'percentage_rule_nodes': result})

@analysis_bp.route('/percentage_derived_nodes', methods=['GET'])
def percentage_derived_nodes():
    global LAG
    numDerived = 0
    for key in LAG:
        numDerived += (LAG[key].node_type == DataDriven.Node_Type.DERIVED)
    
    result=round((float(numDerived) / float(len(LAG)) * 100.0),3)
    return jsonify({'percentage_derived_nodes': result})

@analysis_bp.route('/network_entropy', methods=['GET'])
def network_entropy():
    global LAG
    net_entropy = [0.0,0.0,0.0]
    for key in LAG:
        for i in range(3):
            net_entropy[i] += LAG[key].derived_score[i] * math.log2(LAG[key].derived_score[i])
    
    for i in range(3):
        net_entropy[i] *= -1.0
        
    result = [] 
    result.append({'base' : round(net_entropy[0],3)})
    result.append({'exploitability' : round(net_entropy[1],3)})
    result.append({'impact' : round(net_entropy[2],3)})

    return jsonify({'network_entropy': result})


################## MODEL DRIVEN ##############################
vulnerability_graph = []        # dictionary of nodes
class ModelDriven:
    # Enum for node layers
    class Layers(Enum):
        ROMOTE_ATTACKER = auto()
        CORPORATE_FIREWALL_FW1 = auto()
        CORPORATE_DMZ = auto()
        CORPORATE_FIREWALL_FW2 = auto()
        CORPORATE = auto()
        CONTROL_SYSTEM_FIREWALL_FW1 = auto()
        CONTROL_SYSTEM_DMZ = auto()
        CONTROL_SYSTEM_FIREWALL_FW2 = auto()
        CONTROL_SYSTEM = auto()
        PHYSICAL = auto()

    # object for nodes
    class Node:
        def __init__(self, product, _layer, _index):
            self.out_edges = []              # array of outgoing edges
            self.in_edges = []               # array of incoming edges
            self.discription = product       # node discription
            self.layer = _layer              # what layer does node belong too
            self.index = _index

    # object for weighted edges nodes will use
    class Edge:
        def __init__(self, node_source, node_target):
            self.weights = [0.0,0.0,0.0] # base, exploitability, impact scores
            self.target = node_target    # target node (where the edge connect too)
            self.source = node_source    # source node (where the edge starts)

            target.in_edges.append(self)    # adding incoming edge to target

## depth first traversal
# Will find all paths from origin to GoalNode 
Solution_Path = []
GoalNode = None
def Depth_First_Traversal(node, path):
    # if reached attacker node, stop
    if GoalNode.index == node.index:
        global Solution_Path
        Solution_Path.append(deepcopy(path))
    elif node.layer > GoalNode.layer:
        # determining if deepcopy is needed
        if len(node.in_edges) > 1:
            for n in node.in_edges:
                tmpPath = deepcopy(path)
                tmpPath.append(n)
                Depth_First_Traversal(n.source, tmpPath)
                del tmpPath
        elif len(node.in_edges) == 1:
            path.append(node.in_edges[0])
            Depth_First_Traversal(node.in_edges[0].source, path)

# find exploitability, impact, and base scoes from origin to node
@analysis_bp.route('/model_driven/attack_paths/<node_index>')
def origin_to_node_metrics(node_index):
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # setting calculation variables
    Solution_Path.clear()
    GoalNode = vulnerability_graph[0] # romote attacker node

    # generates solution paths    
    Depth_First_Traversal(vulnerability_graph[node_index], [])

    # calculating metrics
    metrics_per_path = []           # scores from each solution path
    exploitability_list = []
    impact_list = []
    score_sum = [0.0,0.0,0.0]       # used for average length of attack paths

    for path in Solution_Path:
        # tuple for base, exploitability, impact
        score = (0.0,0.0,0.0)

        # pairwise variables used to find top most vulnerable paths
        exploitability_pair = (len(metrics_per_path),0.0)
        impact_pair = (len(metrics_per_path),0.0)

        for edge in path:
            # summing scores from edges
            for i in len(score):
                score[i] += edge.weights[i]
        
        # adding score to cumulative sum
        for i in len(score):
            score_sum[i] += score[i]

        metrics_per_path.append({
                'base_score' : round(score[0],3),
                'exploitability_score' : round(score[1],3),
                'impact_score' : round(score[2],3)
                })
        exploitability_pair[1] = round(score[1],3)
        impact_pair[1] = round(score[2],3)

        exploitability_list.append(exploitability_pair)
        impact_list.append(impact_pair)

    
    ## finding top 5 most vulnerable paths
    # sorting lists in decending order
    exploitability_list.sort(key=lambda vul: vul[1],reverse=True)
    impact_list.sort(key=lambda vul: vul[1],reverse=True)

    # exploitable paths
    top_exploitable = []
    if len(exploitability_list) > 5:
        for i in range(5):
            path = []
            for edge in Solution_Path[exploitability_list[i][0]]:
                path.append(edge.target.index)
            
            top_exploitable.append(path)
    else:
        for i in range(len(exploitability_list)):
            path = []
            for edge in Solution_Path[exploitability_list[i][0]]:
                path.append(edge.target.index)
            
            top_exploitable.append(path) 
    
    # impactful paths
    top_impactful = []
    if len(impact_list) > 5:
        # sorting lists in decending order
        for i in range(5):
            path = []
            for edge in Solution_Path[impact_list[i][0]]:
                path.append(edge.target.index)
            
            top_impactful.append(path)
    else:
        for i in range(len(exploitability_list)):
            path = []
            for edge in Solution_Path[impact_list[i][0]]:
                path.append(edge.target.index)
            
            top_impactful.append(path) 
    
    
    return jsonify({
        'metrics_per_path': metrics_per_path,
        'number_attack_paths' : len(Solution_Path),
        'averge_length_attack_paths' : [
            round(score_sum[0] / len(Solution_Path),3), 
            round(score_sum[1] / len(Solution_Path),3), 
            round(score_sum[2] / len(Solution_Path),3)
            ],
        'top_exploitable': {
            "1" : top_exploitable[0],
            "2" : top_exploitable[1],
            "3" : top_exploitable[2],
            "4" : top_exploitable[3],
            "5" : top_exploitable[4],
        }, 
        'top_impactful': {
            "1" : top_impactful[0],
            "2" : top_impactful[1],
            "3" : top_impactful[2],
            "4" : top_impactful[3],
            "5" : top_impactful[4],
        }})

## Vulnerable Host Percentage Metrics
@analysis_bp.route('/model_driven/vulnerable_host_percentage')
def vulnerable_host_percentage():
    global vulnerability_graph
    node_w_in_edge = set()

    # counting number of nodes with incoming edges
    for node in vulnerability_graph:
        for edge in node.edges:
            if edge.target not in node_w_in_edge:
                node_w_in_edge.add(edge.target)

    # calculating number of vulnerable hosts (nodes with incoming edges) and num of hosts (nodes with no incoming edges)
    number_vulnerable_hosts = len(node_w_in_edge)
    number_hosts = len(vulnerability_graph) - number_vulnerable_hosts

    vulnerable_host_percentage = 100.0 * number_vulnerable_hosts / len(vulnerability_graph)
    non_vulnerable_host_percentage = 100 - vulnerable_host_percentage

    return jsonify({
        'number_vulnerable_hosts': round(number_vulnerable_hosts,3),
        'number_hosts': round(number_hosts,3),
        'vulnerable_host_percentage': round(vulnerable_host_percentage,3),
        'non_vulnerable_host_percentage': round(non_vulnerable_host_percentage,3)
        })


## Centrality Metrics
# Reference: http://www.uvm.edu/pdodds/research/papers/others/2001/brandes2001a.pdf
shortest_paths = []     # matrix where each entry as shortest path value and multiplicity
def betweenness_centrality(node_index):
    global shortest_paths
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # if shortest_paths is empty, then calculate shortest_paths for all nodes
    if len(shortest_paths) == 0:
        # computing the length and number of shortest paths between all pairs
        for source in vulnerability_graph:
            GoalNode = source
            shortest_paths.append([])
            for target in vulnerability_graph:
                if (source == target) or (source.layer >= target.layer):
                    shortest_paths[-1].append((0,0))
                else:
                    Solution_Path.clear()
                    Depth_First_Traversal(target, [])

                    base_sum = []
                    for path in Solution_Path:
                        base_sum.append(0.0)
                        for edge in path:
                            base_sum[-1] += edge.weights[0]
                    
                    base_sum.sort()
                    i = 1
                    # counting number of shortest paths
                    while(base_sum[0] == base_sum[i]):
                        i += 1
                    
                    # adding shortest path
                    shortest_paths[-1].append((base_sum[0],i))
                    
                    del base_sum
    
    # calculating betweeness
    betweenness = 0.0
    for source in vulnerability_graph:
        GoalNode = source
        source_to_v = (0.0,0)
        if source.layer >= vulnerability_graph[node_index].layer or source == vulnerability_graph[node_index]:
            break

        Solution_Path.clear()

        # calculating shortest path from source to v
        Depth_First_Traversal(vulnerability_graph[node_index], [])

        base_sum = []
        for path in Solution_Path:
            base_sum.append(0.0)
            for edge in path:
                base_sum[-1] += edge.weights[0]
        
        base_sum.sort()
        source_to_v[1] = 1
        # counting number of shortest paths
        while(base_sum[0] == base_sum[source_to_v[1]]):
            source_to_v[1] += 1
        
        # saving shortest path and multiplicity
        source_to_v[0] = base_sum[0]

        del base_sum

        for target in vulnerability_graph:
            v_to_target = (0.0,0)

            # target cannot be before node and cannot equal node (node must be between source and target)
            if (target.layer <= vulnerability_graph[node_index].layer or target.layer <= source.layer):
                continue
            
            Solution_Path.clear()
            Depth_First_Traversal(target, [])

            base_sum = []
            for path in Solution_Path:
                base_sum.append(0.0)
                for edge in path:
                    base_sum[-1] += edge.weights[0]
            
            base_sum.sort()
            i = 1
            # counting number of shortest paths
            while(base_sum[0] == base_sum[i]):
                i += 1
            
            # adding shortest path
            shortest_paths[-1].append((base_sum[0],i))
            
            del base_sum
            
            # testing v's betweenness
            if shortest_paths[source.index][target.index] == (v_to_target[0] + source_to_v[0]):
                betweenness += v_to_target[1] * source_to_v[1] / shortest_paths[source.index][target.index][1]
    
    return betweenness

# reference: https://bookdown.org/omarlizardo/_main/4-2-degree-centrality.html
def indegree_centrality(node_index):
    global vulnerability_graph
    return len(vulnerability_graph[node_index].in_edges)

def outdegree_centrality(node_index):
    global vulnerability_graph
    return len(vulnerability_graph[node_index].out_edges) 

# ref: https://mathinsight.org/degree_distribution
def degree_centrality(node_index):
    return indegree_centrality(node_index) + outdegree_centrality(node_index)

# reference: https://en.wikipedia.org/wiki/Centrality
def closeness_centrality(node_index):
    global shortest_paths
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # if shortest_paths is empty, then calculate shortest_paths for all nodes
    if len(shortest_paths) == 0:
        # computing the length and number of shortest paths between all pairs
        for source in vulnerability_graph:
            GoalNode = source
            shortest_paths.append([])
            for target in vulnerability_graph:
                if (source == target) or (source.layer >= target.layer):
                    shortest_paths[-1].append((0,0))
                else:
                    Solution_Path.clear()
                    Depth_First_Traversal(target, [])

                    base_sum = []
                    for path in Solution_Path:
                        base_sum.append(0.0)
                        for edge in path:
                            base_sum[-1] += edge.weights[0]
                    
                    base_sum.sort()
                    i = 1
                    # counting number of shortest paths
                    while(base_sum[0] == base_sum[i]):
                        i += 1
                    
                    # adding shortest path
                    shortest_paths[-1].append((base_sum[0],i))
                    
                    del base_sum
    
    # calculating closeness centrality
    closeness = 0.0
    for y in len(vulnerability_graph):
        dom = 0
        if y < node_index:
            dom = shortest_paths[y][node_index][0]
        else:
            dom = shortest_paths[node_index][y][0]

        if dom > 0:
            closeness += 1/dom

    return closeness

# ref: https://www.geeksforgeeks.org/katz-centrality-centrality-measure/, https://en.wikipedia.org/wiki/Katz_centrality, https://www.youtube.com/watch?v=vSm1a0-VcMg, https://en.wikipedia.org/wiki/Centrality
# calculates katz centrality for all nodes
def katz_centrality_and_pagerank_centrality():
    global vulnerability_graph
    global shortest_paths
    
    def L(mat, row):
        result = 0.0
        for i in len(mat):
            result += mat[row][i]
        return result

    # creating adj_matrix
    adj_mat = np.array([])
    katz = []
    pagerank = []

    for F in shortest_paths:
        adj_mat.append([])
        for T in F:
            adj_mat[-1].append(T[1] > 0)
        
    eigvals, eigvecs = la.eig(adj_mat)

    max_eigval = max(eigvals)

    for i in range(len(adj_mat)):
        katz_tmp = 0.0
        pagarank_tmp = 0.0
        for j in range(len(adj_mat)):
            katz_tmp += adj_mat[i][j] * eigvecs[j]
            pagarank_tmp += adj_mat[i][j] * eigvecs[j] / L(adj_mat, j) + (1 - 1.0 / max_eigval) / len(adj_mat)

        katz.append(1/max_eigval*katz_tmp)
        pagerank.append(1/max_eigval*pagarank_tmp)

    return katz, pagerank

@analysis_bp.route('/model_driven/centrality')   
def centrality():
    pass