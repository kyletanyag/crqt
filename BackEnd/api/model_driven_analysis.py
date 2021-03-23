from flask import Blueprint, jsonify
from enum import IntEnum, auto
from copy import deepcopy 
from collections import deque
import math
import scipy.linalg as la
import numpy as np
import http.client as hc
import json

# route for model driven analysis component
# model_analysis_bp = Blueprint('model_analysis_bp', __name__)


############# MODEL DRIVEN QUERY ###################
httpHost    = "localhost"
port        = 2000
httpMethod  = "GET"

def score_to_weight(score):
    if score >= 0.7:
        return 0.5
    elif score >= 0.4:
        return 0.3
    else:
        return 0.2

# @nvd_bp.route('/model_driven_cvss_query')
def model_driven_cvss_query(vendor, product):
    url = "/api/search/" + vendor + "/" + product

    # Connect to a HTTP server
    hcon = hc.HTTPConnection(httpHost,port)

    # Request for a URL
    hcon.request(httpMethod, url)

    # Get the HTTP response
    response = hcon.getresponse()

    # # Read the HTTP response
    _json = json.loads(response.read().decode('utf-8'))

    weights = []
    scores = []

    # getting scores
    for data in _json["results"]:
        weights.append([0.0,0.0,0.0])
        scores.append([0.0,0.0,0.0])       # base, exploitability, impact

        scores[-1][0] = float(data["cvss"]) / 10.0
        weights[-1][0] = score_to_weight(scores[-1][0])

        scores[-1][1] = float(data["exploitabilityScore"]) / 10.0
        weights[-1][1] = score_to_weight(scores[-1][1])

        scores[-1][2] = float(data["impactScore"]) / 10.0
        weights[-1][2] = score_to_weight(scores[-1][2])
    
    result = [0.0,0.0,0.0]
    weight_sum = [0.0,0.0,0.0]
    # calculating weighted average
    for i in range(len(weights)):
        for j in range(3):
            result[j] += (scores[i][j] * weights[i][j])
            weight_sum[j] += weights[i][j]
    
    for i in range(3):
        result[i] = result[i] / weight_sum[i]

    return result

################## MODEL DRIVEN ##############################
vulnerability_graph = []        # dictionary of nodes
shortest_paths = {}             # matrix where each entry as shortest path value and multiplicity
class ModelDriven:
    # Enum for node layers
    class Layers(IntEnum):
        REMOTE_ATTACK = auto()
        CORP_FW1 = auto()
        CORP_DMZ = auto()
        CORP_FW2 = auto()
        CORP_LAN = auto()
        CS_FW1 = auto()
        CS_DMZ = auto()
        CS_FW2 = auto()
        CS_LAN = auto()

    switch = {
        "remote_attack" : Layers.REMOTE_ATTACK,
        "corp_fw_1" : Layers.CORP_FW1,
        "corp_dmz" : Layers.CORP_DMZ,
        "corp_fw_2" : Layers.CORP_FW2,
        "corp_lan" : Layers.CORP_LAN,
        "cs_fw_1" : Layers.CS_FW1,
        "cs_dmz" : Layers.CS_DMZ,
        "cs_fw_2" : Layers.CS_FW2,
        "cs_lan" : Layers.CS_LAN
    }
    # object for nodes
    class Node:
        def __init__(self, product, vendor, layer, index):
            self.out_edges = []             # array of outgoing edges
            self.in_edges = []              # array of incoming edges
            self.product = product          # node discription
            self.vendor = vendor
            self.index = index
            self.weights = [1.0,1.0,1.0]    # base, exploitability, impact scores

            if product and vendor:
                self.weights = model_driven_cvss_query(vendor, product)

            # determining what layer
            self.layer = ModelDriven.switch[layer]  # what layer does node belong too

    # object for weighted edges nodes will use
    class Edge:
        def __init__(self, node_source, node_target):
            self.target = node_target    # target node (where the edge connect too)
            self.source = node_source    # source node (where the edge starts)

            self.target.in_edges.append(self)    # adding incoming edge to target
            self.source.out_edges.append(self)

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

# will generate shortest path
def shortest_paths_gen():
    global shortest_paths
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # computing the length and number of shortest paths between all pairs
    for source in vulnerability_graph:
        GoalNode = source
        for target in vulnerability_graph:
            if (source == target) or (source.layer >= target.layer):
                continue # shortest_paths[(source.index,target.index)] = (0,0)
            else:
                Solution_Path.clear()
                Depth_First_Traversal(target, [])

                if len(Solution_Path) > 0:
                    base_sum = []
                    for path in Solution_Path:
                        base_sum.append(0.0)
                        for edge in path:
                            base_sum[-1] += edge.target.weights[0]
                    
                    base_sum.sort()
                    i = 1
                    # counting number of shortest paths
                    while(not(i == len(base_sum)) and base_sum[0] == base_sum[i]):
                        i += 1
                    
                    # adding shortest path
                    shortest_paths[(source.index,target.index)] = (base_sum[0],i)
                    del base_sum                

# find exploitability, impact, and base scoes from origin to node
# @model_analysis_bp.route('/model_driven/attack_paths/<node_index>')
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
        score = [0.0,0.0,0.0]

        for edge in path:
            # summing scores from edges
            for i in range(len(score)):
                score[i] += edge.target.weights[i]
        
        # adding score to cumulative sum
        for i in range(len(score)):
            score_sum[i] += score[i]

        metrics_per_path.append({
                'base_score' : round(score[0],3),
                'exploitability_score' : round(score[1],3),
                'impact_score' : round(score[2],3)
                })

        exploitability_list.append([len(metrics_per_path) - 1,round(score[1],3)])
        impact_list.append([len(metrics_per_path) - 1,round(score[2],3)])

    
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
            
            top_exploitable.append({str(i) : path})
    else:
        for i in range(len(exploitability_list)):
            path = []
            for edge in Solution_Path[exploitability_list[i][0]]:
                path.append(edge.target.index)
            
            top_exploitable.append({str(i) : path}) 
    
    # impactful paths
    top_impactful = []
    if len(impact_list) > 5:
        # sorting lists in decending order
        for i in range(5):
            path = []
            for edge in Solution_Path[impact_list[i][0]]:
                path.append(edge.target.index)
            
            top_impactful.append({str(i) : path})
    else:
        for i in range(len(exploitability_list)):
            path = []
            for edge in Solution_Path[impact_list[i][0]]:
                path.append(edge.target.index)
            
            top_impactful.append({str(i) : path})
    
    
    return jsonify({
        'metrics_per_path': metrics_per_path,
        'number_attack_paths' : len(Solution_Path),
        'averge_length_attack_paths' : [
            round(score_sum[0] / len(Solution_Path),3), 
            round(score_sum[1] / len(Solution_Path),3), 
            round(score_sum[2] / len(Solution_Path),3)
            ],
        'top_exploitable': top_exploitable, 
        'top_impactful': top_impactful
        })

## Vulnerable Host Percentage Metrics
# @model_analysis_bp.route('/model_driven/vulnerable_host_percentage')
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
def betweenness_centrality(node_index):
    global shortest_paths
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # if shortest_paths is empty, then calculate shortest_paths for all nodes
    if len(shortest_paths) == 0:
        shortest_paths_gen()
    
    # calculating betweeness
    betweenness = 0.0
    for source in vulnerability_graph:
        # source cannot goto node if on same or greater layer
        if source.layer == vulnerability_graph[node_index].layer:
            break

        for target_id in range(node_index,len(vulnerability_graph)):            
            # testing if path exist between source to node && node to target
            if (all(x in shortest_paths.keys() for x in [(source.index,target_id), (source.index,node_index), (node_index,target_id)])):
                # testing v's betweenness
                if shortest_paths[(source.index,target_id)][0] == (shortest_paths[(source.index,node_index)][0] + shortest_paths[(node_index,target_id)][0]):
                    betweenness += shortest_paths[(source.index,node_index)][1] * shortest_paths[(node_index,target_id)][1] / shortest_paths[(source.index,target_id)][1]
    
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
        shortest_paths_gen()
    
    # calculating closeness centrality
    closeness = 0.0
    for y in len(vulnerability_graph):
        dist = 0
        if y < node_index:
            dist = shortest_paths[(y,node_index)][0]
        else:
            dist = shortest_paths[(node_index,y)][0]

        if dist > 0:
            closeness += 1.0/dist

    return closeness

# ref: 
# [1] https://ocw.mit.edu/courses/civil-and-environmental-engineering/1-022-introduction-to-network-models-fall-2018/lecture-notes/MIT1_022F18_lec4.pdf, 
# [2] https://www.nature.com/articles/s41598-017-15426-1
# https://www.youtube.com/watch?v=vSm1a0-VcMg, 
# [4] https://en.wikipedia.org/wiki/Centrality
# 
# calculates katz centrality for all nodes
def katz_centrality_and_pagerank_centrality():
    global vulnerability_graph
    global shortest_paths
    
    def L(mat, row):
        result = 0.0
        for i in range(len(mat)):
            result += mat[row][i]
        return result

    # creating adj_matrix
    adj_mat = np.zeros((len(vulnerability_graph),len(vulnerability_graph)),dtype=np.uint8)
    pagerank = []


    for node in vulnerability_graph:
        for edge in node.out_edges:
            adj_mat[node.index][edge.target.index] = 1
    
    # calculating eigenvectors/values
    eigvals, eigvecs = la.eig(adj_mat)

    # finding max eigenvalue
    max_eigval = max(eigvals)

    alpha = 0.0 
    if max_eigval == 0j:    # if eigenval is zero
        alpha = 1.0
    else:
        alpha = 1.0/max_eigval - 0.01
        if alpha > 1:
            alpha = 1.0

    # calculating Katz = inv(I - a*A)*vec(n,1) Ref: [1][2]
    katz = np.dot(la.inv(np.subtract(np.identity(len(adj_mat)), 1.0/alpha * adj_mat)),np.ones((len(adj_mat),1)))

    norm = 0.0
    # normalizing katz vector
    for val in katz:
        norm += val**2
    katz *= 1.0 / math.sqrt(norm)

    # calculating pagerank
    norm = 0.0
    for i in range(len(adj_mat)):
        # katz_tmp = 0.0
        pagarank_tmp = 0.0
        for j in range(len(adj_mat)):
            # katz_tmp += adj_mat[i][j] * eigvecs[j]
            pagarank_tmp += adj_mat[i][j] * eigvecs[j] / L(adj_mat, j) + (1 - 1.0 / alpha) / len(adj_mat)

        # katz.append(1/max_eigval*katz_tmp)
        pagerank.append(1/alpha*pagarank_tmp)
        norm += (1/alpha*pagarank_tmp) ** 2 

    # normalizing pagerank 
    norm = 1.0/math.sqrt(norm)
    for page in pagerank:
        page *= norm

    return katz, pagerank

# @model_analysis_bp.route('/model_driven/centrality')   
def centrality():
    pass

def TOPSIS():
    pass