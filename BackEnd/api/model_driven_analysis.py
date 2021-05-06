'''
@author Thomas J. Laverghetta
@brief Contains all functions for analyzing model-driven inputs.
These include:
- attack path metrics
- vulnerability percentage metric
- TOPSIS
- graph centrality metrics

'''

from flask import Blueprint, jsonify
from .nvd import model_driven_cvss_query 
from .round_sig import round_sig
from enum import IntEnum, auto
from copy import deepcopy 
from collections import deque
import math
import scipy.linalg as la
import numpy as np
import time

# route for model driven analysis component
model_analysis_bp = Blueprint('model_analysis_bp', __name__)

################## MODEL DRIVEN ##############################
# calculating variables
vulnerability_graph = []        # dictionary of nodes
shortest_paths = {}             # matrix where each entry as shortest path value and multiplicity
Solution_Path = deque()         # used for depth-first traversal, gives solution paths from target to goal (source)
GoalNode = None                 # goal (source) node for depth-first traversal
centrality_metrics = []         # holds the centrality metrics (betweeness, indegree, outdegree, degree, closeness, pagerank, katz)
topsis_metrics = []             # holds the topsis method metrics

# timing metrics
shortest_path_time = None       # computation time to compute shortest_paths
centrality_time = None            # computation time to compute all centrality metrics
topsis_time = 0.0               # computation time to compute topsis metrics

# model driven data-structure 
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

    # switch for converting layers string to enum
    switch = {
        "remote_attack" : Layers.REMOTE_ATTACK,
        "corp_fw_1"     : Layers.CORP_FW1,
        "corp_dmz"      : Layers.CORP_DMZ,
        "corp_fw_2"     : Layers.CORP_FW2,
        "corp_lan"      : Layers.CORP_LAN,
        "cs_fw_1"       : Layers.CS_FW1,
        "cs_dmz"        : Layers.CS_DMZ,
        "cs_fw_2"       : Layers.CS_FW2,
        "cs_lan"        : Layers.CS_LAN
    }

    # object for nodes
    class Node:
        def __init__(self, product, vendor, layer, index, cve_ids, product_type):
            self.out_edges = []             # array of outgoing edges
            self.in_edges = []              # array of incoming edges
            self.product = product          # node product
            self.type = product_type
            self.vendor = vendor            # node vendor
            self.index = index              # node index/id
            self.weights = np.array([1.0,1.0,1.0])    # base, exploitability, impact scores

            if cve_ids:
                self.weights = model_driven_cvss_query(cve_ids)

            # determining what layer
            self.layer = ModelDriven.switch[layer]  # what layer does node belong too

    # object for weighted edges nodes will use
    class Edge:
        def __init__(self, node_source, node_target):
            self.target = node_target       # target node (where the edge connect too)
            self.source = node_source       # source node (where the edge starts)
            
            self.target.in_edges.append(self)       # adding incoming edge to target
            self.source.out_edges.append(self)      # adding out edges to source

# will send graph topology to front-end
@model_analysis_bp.route('/model_driven/get_network_topology', methods=['GET'])
def get_network_topology():
    global vulnerability_graph

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

    vertices = []
    edges = []
    # creating json with vertices and arcs objects 
    for node in vulnerability_graph: 
        vertices.append({
            'id'        : node.index,
            'vendor'    : node.vendor,
            'product'   : node.product,
            'layer'     : switch[node.layer],
            'type'      : node.type           
        })
        for e in node.out_edges:
            edges.append({
                'source'                : node.index,
                'target'                : e.target.index,
                'base_score'            : round_sig(e.target.weights[0],3),
                'exploitability_score'  : round_sig(e.target.weights[1],3),
                'impact_score'          : round_sig(e.target.weights[2],3)
            })
    
    return {'nodes': vertices, 'edges' : edges}, 200

# initializing all global variables
def ModelDriven_init():
    global vulnerability_graph
    global shortest_paths
    global Solution_Path
    global centrality_metrics
    global shortest_path_time
    global topsis_metrics
    global topsis_time

    vulnerability_graph.clear()
    shortest_paths.clear()
    Solution_Path.clear()
    centrality_metrics.clear()
    topsis_metrics.clear()
    shortest_path_time = 0.0
    centrality_time = 0.0
    topsis_time = 0.0

## depth first traversal
# Will find all paths from target to source (goal node) 
# starts at target node and traverses backwords through network (i.e., target to source)
MAX_NUM_PATHS=100
def Depth_First_Traversal(node, path, score):
    # if reached attacker node, stop
    if GoalNode.index == node.index:
        global Solution_Path
        Solution_Path.append((deepcopy(path),deepcopy(score)))
    elif node.layer > GoalNode.layer:
        score += node.weights
        path.append(node.index)
        
        for n in node.in_edges:
            Depth_First_Traversal(n.source, path, score)
        
        path.pop()
        score -= node.weights

# used for shortest path generation (takes into account score that standard does not)
def Short_Path_Depth_First_Traversal(InitNode, goal):
    global vulnerability_graph
    extended = dict()   # set of extended nodes and their scores
    queue = list()      # queue of nodes and their scores
    shortest = np.array([50.0,0]) # shortest score and multiplicity

    queue.append((InitNode,0.0))
    currLayer = InitNode.layer
    while len(queue):
        node, score = queue.pop(0)
        
        if currLayer > node.layer:
            extended.clear()
            currLayer = node.layer

        # if reached goal node node, stop
        if goal.index == node.index and shortest[0] >= score:
            # if the score calculated smaller than current smallest, set score to smallest and reset number of paths found with that score 
            if score < shortest[0]:
                shortest[0] = score
                shortest[1] = 1
            # else, increase number of paths with this score
            else:
                shortest[1] += 1
        
        elif shortest[0] >= score and node.layer > goal.layer:
            # accumulating score from this node (edge weight)
            score += (1 - node.weights[0])          # 1 - CVSS/10

            for n in node.in_edges:
                if n.source.index not in extended:
                    queue.append((n.source, deepcopy(score)))
                    extended[n.source.index] = score
                elif extended[n.source.index] > score:
                    i = queue.index((n.source,extended[n.source.index]))
                    del queue[i]
                    queue.append((n.source, deepcopy(score)))
                    extended[n.source] = score
    
    return shortest[0], shortest[1]

# will generate shortest paths
def shortest_paths_gen():
    global shortest_paths
    global vulnerability_graph
    global shortest_path_time

    # starting timer for process time calc
    start_timer = time.time()

    # computing the length and number of shortest paths between all pairs
    for source in vulnerability_graph:
        GoalNode = source
        for target in vulnerability_graph[(source.index+1):]:
            # no path exists if source is target or source is on same or greater layer than target
            if source.layer < target.layer:              
                score, multiplicity = Short_Path_Depth_First_Traversal(target, source)

                if multiplicity > 0:                    
                    # adding shortest path
                    shortest_paths[(source.index,target.index)] = (score, multiplicity)

    # calc process time
    shortest_path_time = time.time() - start_timer

@model_analysis_bp.route('/model_driven/attack_paths/get_shortest_path_computation_time', methods=['GET'])
def shortest_path_comp_time():
    global shortest_path_time
    return jsonify({'shortest_path_computation_time' : round_sig(shortest_path_time,4)})

# find exploitability, impact, and base scoes from origin to node
@model_analysis_bp.route('/model_driven/attack_paths/<node_index>', methods=['GET'])
def origin_to_node_metrics(node_index):
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # starting timer for processing time calculation
    start_timer = time.time()

    # setting calculation variables
    Solution_Path.clear()
    GoalNode = vulnerability_graph[0] # romote attacker node

    # generates solution paths    
    Depth_First_Traversal(vulnerability_graph[int(node_index)], deque(), np.array([0.0,0.0,0.0]))

    # calculating metrics
    metrics_per_path = []           # scores from each solution path
    exploitability_list = [(0, 0.0) for x in range(5)] # top 5 most exploitable paths
    impact_list = [(0, 0.0) for x in range(5)]         # top 5 most impactful paths
    score_sum = np.array([0.0,0.0,0.0]) # used for average length of attack paths
    
    # score = np.array([0.0,0.0,0.0])     # tuple for base, exploitability, impact
    count = 0
    number_paths = len(Solution_Path)
    while len(Solution_Path):
        path = Solution_Path.pop()
        score = path[1]
        # score = np.sum([edge.target.weights for edge in path], axis=0)
        
        # adding score to cumulative sum
        score_sum += score
        
        metrics_per_path.append({
            'path_id' : count + 1,
            'path'    : [x for x in path[0]],
            'base_score' : round_sig(score[0],3),
            'exploitability_score' : round_sig(score[1],3),
            'impact_score' : round_sig(score[2],3)
        })

        # sorted insert for top exploitable/impactful paths
        if exploitability_list[4][1] < score[1]:   # if last most exploitable is less than current path
            # check each exploitable path saved and compare with curr path
            for i in range(5):
                # if curr is less exploitable than next exploitable, replace curr exploitable with curr path and del last element
                if i == 0 or exploitability_list[i-1][1] >= score[1]:
                    exploitability_list.insert(i, (count,round_sig(score[1],3)))
                    del exploitability_list[-1]
                    break

        if impact_list[4][1] < score[2]:
            for i in range(5):
                if i == 0 or impact_list[i-1][1] >= score[2]:
                    impact_list.insert(i, (count,round_sig(score[2],3)))
                    del impact_list[-1]
                    break
        
        count += 1

    # exploitable paths
    top_exploitable = []
    for ex in exploitability_list[:5]:
        if ex[1] == 0.0:
            break

        top_exploitable.append({str(ex[0]+1) : metrics_per_path[ex[0]]['path'], "exploitability" : ex[1]}) 
    
    # impactful paths
    top_impactful = []
    for im in impact_list[:5]:
        if im[1] == 0.0:
            break
        
        top_impactful.append({str(im[0] + 1) : metrics_per_path[im[0]]['path'], "impact" : im[1]})
    
    # calculating processing time
    processing_time = time.time() - start_timer
    
    return {
        'metrics_per_path': metrics_per_path,
        'number_attack_paths' : number_paths,
        'averge_length_attack_paths' : [
            round_sig(score_sum[0] / number_paths,3), 
            round_sig(score_sum[1] / number_paths,3), 
            round_sig(score_sum[2] / number_paths,3)
            ],
        'top_exploitable': top_exploitable, 
        'top_impactful': top_impactful,
        'computation_time' : round_sig(processing_time,4)
        }

## Vulnerable Host Percentage Metrics
@model_analysis_bp.route('/model_driven/vulnerable_host_percentage', methods=['GET'])
def vulnerable_host_percentage():
    global vulnerability_graph

    # starting the timer for processing time calculation
    start_timer = time.time()

    # counting number of nodes with incoming edges
    number_vulnerable_hosts = sum(len(node.in_edges) > 0 for node in vulnerability_graph)

    # num of hosts (all nodes except remote)
    number_hosts = len(vulnerability_graph) - 1

    vulnerable_host_percentage = 100.0 * number_vulnerable_hosts / number_hosts
    non_vulnerable_host_percentage = 100 - vulnerable_host_percentage

    # processing time calc
    processing_time = time.time() - start_timer

    return jsonify({
        'number_vulnerable_hosts': round_sig(number_vulnerable_hosts,3),
        'number_hosts': round_sig(number_hosts,3),
        'vulnerable_host_percentage': round_sig(vulnerable_host_percentage,3),
        'non_vulnerable_host_percentage': round_sig(non_vulnerable_host_percentage,3),
        'computation_time' : round_sig(processing_time,4)
        })

## Centrality Metrics
# Reference: http://www.uvm.edu/pdodds/research/papers/others/2001/brandes2001a.pdf
def betweenness_centrality():
    global shortest_paths
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # if shortest_paths is empty, then calculate shortest_paths for all nodes
    if len(shortest_paths) == 0:
        shortest_paths_gen()

    # calculating betweeness
    betweenness = []
    for node in vulnerability_graph:
        betweenness.append(0.0)
        for source in vulnerability_graph[:(node.index)]:
            # no path exist if node and source are on same layer
            # if source.layer == vulnerability_graph[node.index].layer:
            #     break

            for target in vulnerability_graph[(node.index+1):]:      
                # target cannot equal source (no path) and no path exist if target and node are same layer
                if target.layer > vulnerability_graph[node.index].layer: 
                    # testing if path exist between source to node && node to target
                    # shortest_paths is a multi-key dictionary with key 1 = source and key 2 = target. 
                    # therefore, check if paths between (source, target) and (source, node) and (node, target) exist following betweeness equation
                    if (all(x in shortest_paths.keys() for x in [(source.index,target.index), (source.index,node.index), (node.index,target.index)])):
                        # testing v's betweenness
                        if shortest_paths[(source.index,target.index)][0] == (shortest_paths[(source.index,node.index)][0] + shortest_paths[(node.index,target.index)][0]):
                            betweenness[-1] += shortest_paths[(source.index,node.index)][1] * shortest_paths[(node.index,target.index)][1] / shortest_paths[(source.index,target.index)][1]
    
    return betweenness

# ref: https://bookdown.org/omarlizardo/_main/4-2-degree-centrality.html
# https://mathinsight.org/degree_distribution
def degree_centrality():
    global vulnerability_graph
    indegree = []
    outdegree = []
    degree = []

    # calculating degree centrality (in, out, and combined)
    for node in vulnerability_graph:
        indegree.append(len(vulnerability_graph[node.index].in_edges))
        outdegree.append(len(vulnerability_graph[node.index].out_edges))
        degree.append(indegree[-1] + outdegree[-1])

    return [indegree, outdegree, degree]

# reference: https://en.wikipedia.org/wiki/Centrality
def closeness_centrality():
    global shortest_paths
    global Solution_Path
    global vulnerability_graph
    global GoalNode

    # if shortest_paths is empty, then calculate shortest_paths for all nodes
    if len(shortest_paths) == 0:
        shortest_paths_gen()
    
    # calculating closeness centrality
    closeness = []
    for node in vulnerability_graph:
        node_index = node.index
        dist = 0.0
        for y in range(len(vulnerability_graph)):
            
            # calculating the distance between node and y
            # since shortest_path does source to target where source index < target index:
            # therefore, index has to be tested to determine source and target, respectively
            if y < node_index:
                if (y,node_index) in shortest_paths.keys(): 
                    dist += shortest_paths[(y,node_index)][0]
            else:
                if (node_index,y) in shortest_paths.keys():
                    dist += shortest_paths[(node_index,y)][0]

        if dist > 0.0:
            closeness.append(1.0/dist)
        else: # unconnected node, no path distance
            closeness.append(math.inf)

    return closeness

# ref: 
# [1] https://ocw.mit.edu/courses/civil-and-environmental-engineering/1-022-introduction-to-network-models-fall-2018/lecture-notes/MIT1_022F18_lec4.pdf, 
# [2] https://www.nature.com/articles/s41598-017-15426-1
# https://www.youtube.com/watch?v=vSm1a0-VcMg, 
# calculates katz centrality for all nodes
def katz_centrality():
    global vulnerability_graph
    
    # creating adj_matrix
    adj_mat = np.zeros((len(vulnerability_graph),len(vulnerability_graph)),dtype=np.uint8)

    for node in vulnerability_graph:
        for edge in node.out_edges:
            adj_mat[node.index][edge.target.index] = 1
    
    # calculating eigenvectors/values
    eigvals, eigvecs = la.eig(adj_mat)

    # finding max eigenvalue
    max_eigval = max(eigvals)

    alpha = 0.0 
    if max_eigval == 0j:    # if eigenval is zero
        alpha = 0.1
    else:
        alpha = 1.0/max_eigval
        if alpha > 1:
            alpha = 0.1

    # calculating Katz = inv(I - a*A)*vec(n,1) Ref: [1],[2]
    katz = np.dot(la.inv(np.subtract(np.identity(len(adj_mat)), 1.0/alpha * adj_mat)),np.ones((len(adj_mat),1)))

    norm = 0.0
    # normalizing katz vector
    for val in katz:
        norm += val**2
    katz *= 1.0 / math.sqrt(norm)

    return katz

# ref: https://methods.sagepub.com/base/download/DatasetStudentGuide/pagerank-in-florentine-1994-python
# http://infolab.stanford.edu/~backrub/google.html
# d is damping factor in set (0,1) default val is 0.85
def pagerank_centrality(d=0.85):
    global vulnerability_graph

    # PageRank: PR(A) = (1-d) + d (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))
    # where page A has pages T1...Tn which point to it and C(A) is outdegree
    pagerank = np.zeros((len(vulnerability_graph),), dtype=float)
    for node in vulnerability_graph:
        pagerank[node.index] = sum(pagerank[inedge.source.index] / len(inedge.source.out_edges) for inedge in node.in_edges)

        pagerank[node.index] *= d
        pagerank[node.index] += 1.0-d

    # normalizing pagerank 
    pagerank *= 1.0/math.sqrt(np.sum(pagerank ** 2))

    return pagerank

@model_analysis_bp.route('/model_driven/centrality', methods=['GET'])   
def centrality():
    global centrality_metrics # holds the centrality metrics (betweeness, indegree, outdegree, degree, closeness, katz, pagerank)
    global vulnerability_graph
    global shortest_path_time
    global centrality_time


    # if centrality metrics have not been calculated, then calculate them for all nodes
    if len(centrality_metrics) == 0:
        # starting timer for centrality metrics
        start_timer = time.time()

        centrality_metrics.append(betweenness_centrality())
        degree = degree_centrality()
        for i in range(3):
            centrality_metrics.append(degree[i])

        centrality_metrics.append(closeness_centrality())
        centrality_metrics.append(pagerank_centrality())
        centrality_metrics.append(katz_centrality())

        centrality_time = time.time() - start_timer
    
    return jsonify({
        "betweeness": [round_sig(x,3) for x in centrality_metrics[0]],
        "indegree"  : [round_sig(x,3) for x in centrality_metrics[1]],
        "outdegree" : [round_sig(x,3) for x in centrality_metrics[2]],
        "degree"    : [round_sig(x,3) for x in centrality_metrics[3]],
        "closeness" : [round_sig(x,3) for x in centrality_metrics[4]],
        "pagerank"  : [round_sig(x,3) for x in centrality_metrics[5]],
        "katz"      : [round_sig(x[0],3) for x in centrality_metrics[6]],
        "shortest_path_computation_time" : round_sig(shortest_path_time,4),
        "centrality_computation_time" : round_sig(centrality_time,4)
    })
    

# ref: Modeling Cyber Resilience for Energy Delivery Systems using critical system functionality      
@model_analysis_bp.route('/model_driven/topsis', methods=['GET'])
def TOPSIS():
    from .topsis import topsis
    global centrality_metrics
    global vulnerability_graph
    global topsis_metrics
    global topsis_time

    if len(topsis_metrics) == 0:
        if len(centrality_metrics) == 0:
            centrality()

        # start timer for process time calc 
        start_timer = time.time()

        # constructing matrix (criteria and alternatives) 
        # matrix will contain all nodes except remote for alternative nodes
        # criteria are exploitability, impact, betweeness centrality, and katz centrality
        a = []
        # appending node exploitability and impact scores
        a.append([])
        a.append([]) 
        for node in vulnerability_graph[1:]:
            a[0].append(node.weights[1])    # appending node's exploitability
            a[1].append(node.weights[2])    # appending node's impact

        a.append(centrality_metrics[0][1:]) # appending betweeness centrality excluding remote
        a.append([])
        for val in centrality_metrics[6][1:]:
            a[-1].append(val[0])                   # appending katz centrality excluding remote

        # constructing weights array: this will follow Arif's work done in ref
        w = [0.25,0.5,0.15,0.1]    

        # positive impact matrix, following Mathemtical Modeling in Social Network Analysis: Using TOPSIS to Find Node influences in social ndetwork
        # p. 537
        j = np.ones((len(a),), dtype=int)    

        t = topsis(a,w,j)
        n = t.calc()        # calculating topsis, n is array of criticalities of each node

        for i in range(len(n)):
            topsis_metrics.append({"node_id" : i + 1, "topsis_score": round_sig(n[i],3)})

        topsis_time = time.time() - start_timer
    return jsonify({
        "topsis" : topsis_metrics,
        "topsis_computation_time" : round_sig(topsis_time,4)
    })
