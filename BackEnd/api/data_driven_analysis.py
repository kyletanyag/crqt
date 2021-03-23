from flask import Blueprint, jsonify, request
from enum import Enum, auto
from copy import deepcopy 
from collections import deque
from . import db 
import math
import scipy.linalg as la
import numpy as np

# route for LAG generation module
data_analysis_bp = Blueprint('data_analysis_bp', __name__)

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

@data_analysis_bp.route('/data_driven/getDerivedScores', methods=['GET'])
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

@data_analysis_bp.route('/data_driven/test-derived-scores', methods=['GET'])
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
@data_analysis_bp.route('/data_driven/percentage_execCode_nodes', methods=['GET'])
def percentage_execCode_nodes():
    global LAG
    sum = 0
    for key in LAG:
        sum += LAG[key].isExecCode

    result=round((float(sum) / float(len(LAG)) * 100.0),3)
    print(sum)
    return jsonify({'percentage_execCode_nodes': result})

# returns the execCode nodes with their probabilities
@data_analysis_bp.route('/data_driven/execCode_node_probabilities', methods=['GET'])
def execCode_node_probabilities():
    global LAG

    vertices = []
    for key in LAG: 
        if LAG[key].isExecCode:
            vertices.append({
                'id' : key,
                'discription' : LAG[key].discription,
                'node_type' : 'Derived Fact', 
                'base_score' : round(LAG[key].derived_score[0],3),
                'exploitability_score' : round(LAG[key].derived_score[1],3),
                'impact_score' : round(LAG[key].derived_score[2],3)})
    
    return jsonify({'nodes': vertices})

# returns the derived nodes with their probabilities
@data_analysis_bp.route('/data_driven/derived_node_probabilities', methods=['GET'])
def derived_node_probabilities():
    global LAG

    vertices = []
    for key in LAG: 
        if LAG[key].node_type == DataDriven.Node_Type.DERIVED:
            vertices.append({
                'id' : key,
                'discription' : LAG[key].discription,
                'node_type' : 'Derived Fact', 
                'base_score' : round(LAG[key].derived_score[0],3),
                'exploitability_score' : round(LAG[key].derived_score[1],3),
                'impact_score' : round(LAG[key].derived_score[2],3)})
    
    return jsonify({'nodes': vertices})

@data_analysis_bp.route('/data_driven/percentage_rule_nodes', methods=['GET'])
def percentage_rule_nodes():
    global LAG
    rules = 0
    for key in LAG:
        rules += (LAG[key].node_type == DataDriven.Node_Type.DERIVATION)

    result=round((float(rules) / float(len(LAG)) * 100.0),3)
    return jsonify({'percentage_rule_nodes': result})

@data_analysis_bp.route('/data_driven/percentage_derived_nodes', methods=['GET'])
def percentage_derived_nodes():
    global LAG
    numDerived = 0
    for key in LAG:
        numDerived += (LAG[key].node_type == DataDriven.Node_Type.DERIVED)
    
    result=round((float(numDerived) / float(len(LAG)) * 100.0),3)
    return jsonify({'percentage_derived_nodes': result})

@data_analysis_bp.route('/data_driven/network_entropy', methods=['GET'])
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