from flask import Blueprint, jsonify, request
import enum
from copy import deepcopy 
from collections import deque
from . import db 
import math

# route for LAG generation module
analysis_bp = Blueprint('analysis_bp', __name__)

# namespace for data-driven objects
class DataDriven:
    # Enum for node relationships
    class Node_Logic(enum.Enum):
        AND = 0
        OR = 1
        FLOW = 2
        LEAF = 3

    # Enum for Node Types
    class Node_Type(enum.Enum):
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
    class Layers(enum.Enum):
        ROMOTE_ATTACKER = 0
        CORPORATE_DMZ = 1
        CORPORATE = 2
        CONTROL_DMZ = 3
        CONTROL = 4
        PHY = 5

    class Node:
        def __init__(self):
            edges = []              # array of edges
            discription = str()     # node discription
            layer = None            # what layer does node belong too
            index = int()

        class Edge:
            def __init__(self, node_target):
                weights = [0.0,0.0,0.0] # base, exploitability, impact scores
                target = node_target    # target node (where the edge connect too)
                source = None

## depth first traversal
# Will find all paths from origin to GoalNode 
Solution_Path = []
GoalNode = int()
def Depth_First_Traversal(node, path):
    global GoalNode
    if GoalNode == node.index:
        global Solution_Path
        Solution_Path.append(deepcopy(path))
    
    # verifying node is below goal node layer
    elif node.layer < vulnerability_graph[GoalNode].layer:
        # determining if deepcopy is needed
        if len(node.edges) > 1:
            for n in node.edges:
                tmpPath = deepcopy(path)
                tmpPath.append(n)
                Depth_First_Traversal(n.target, n)
                del tmpPath
        elif len(node.edge) == 1:
            path.append(node.edge[0])
            Depth_First_Traversal(node.edge[0].target, path)

# find exploitability, impact, and base scoes from origin to node
@analysis_bp.route('/model_driven/attack_paths/<node_index>')
def origin_to_node_metrics(node_index):
    global Solution_Path
    global GoalNode
    global vulnerability_graph

    # setting calculation variables
    GoalNode = node_index
    Solution_Path.clear()

    # generates solution paths    
    Depth_First_Traversal(vulnerability_graph[0], [])

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
                path.append(edge.source.index)
            
            top_exploitable.append(path)
    else:
        for i in range(len(exploitability_list)):
            path = []
            for edge in Solution_Path[exploitability_list[i][0]]:
                path.append(edge.source.index)
            
            top_exploitable.append(path) 
    
    # impactful paths
    top_impactful = []
    if len(impact_list) > 5:
        # sorting lists in decending order
        for i in range(5):
            path = []
            for edge in Solution_Path[impact_list[i][0]]:
                path.append(edge.source.index)
            
            top_impactful.append(path)
    else:
        for i in range(len(exploitability_list)):
            path = []
            for edge in Solution_Path[impact_list[i][0]]:
                path.append(edge.source.index)
            
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
