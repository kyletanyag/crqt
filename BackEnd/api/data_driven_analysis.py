from flask import Blueprint, jsonify, request
from enum import Enum, auto
from copy import deepcopy 
from collections import deque
from . import db 
import math
import requests
import time

# route for LAG generation module
data_analysis_bp = Blueprint('data_analysis_bp', __name__)
LAG = []
derived_score_computation_time = 0.0

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

    switch = {
        "FLOW"  : Node_Logic.FLOW,
        "AND"   : Node_Logic.AND,
        "LEAF"  : Node_Logic.LEAF,
        "OR"    : Node_Logic.OR
    }

    # graph data structure (adjenency list) for DataDriven
    class Node:
        def __init__(self, index, logic, discription):
            self.index = index                      # node index
            self.derived_score = [1.0,1.0,1.0]      # base, exploitability, impact scores
            self.description = discription          # node description
            self.node_type = None                   # type of node  
            self.node_logic = DataDriven.switch[logic]# node relationship 
            self.next_node = []                     # next nodes
            self.calculations_remaining = 0         # number of nodes needed to calculate derived score
            self.isExecCode = False                 # whether node is execCode node (used for percentage execCode metric)
            self.tolNumConditions = 0               # total num of conditions to reach node
            self.diNumConditions = 0                # direct number of conditions to reach node

        def printFunc(self):
            print(self.derived_score, self.description, self.node_type, self.node_logic, self.next_node, self.calculations_remaining, self.isExecCode)

    # object for edges nodes will use
    class Edge:
        def __init__(self, node_source, node_target):
            self.target = node_target    # target node (where the edge connect too)
            self.source = node_source    # source node (where the edge starts)

            self.target.in_edges.append(self)    # adding incoming edge to target
            self.source.out_edges.append(self)

def DataDriven_init():
    global LAG
    global derived_score_computation_time

    LAG.clear()
    derived_score_computation_time = 0.0

'''
Probability Formulas:
For any n events e1, e2, ..., en:
	1. P(e1, e2, ..., en)=product(P(ei),1,n)				    // product (expression, lower, upper)
	2. P(e1 U e2 U ... U en) = 1 - product(P(NOT(ei)),1,n)		// http://people.duke.edu/~hpgavin/cee201/ProbabilityRules.pdf
'''

# scores is derived scores tuple
def Depth_First_Alg(scores, tolNumConditions, node): 
    # reduce number of nodes needed to make calculation
    node.calculations_remaining -= 1
    
    # adding number of conditions to reach node
    node.tolNumConditions += tolNumConditions

    # modifying score
    if node.node_logic == DataDriven.Node_Logic.OR:
        # OR = (1-p1)*...*(1-pn)
        for i in range(3):
           node.derived_score[i] = node.derived_score[i]*(1-scores[i])     # probability formula 2
    else: # node_log == AND OR FLOW
        # AND = p1*...*pn
        for i in range(3):
            node.derived_score[i] = node.derived_score[i]*scores[i]         # probability formula 1
      
    # if no more nodes are required to make calculation
    if node.calculations_remaining == 0:
        # if OR node, then finalize calculation
        # 1 - (1-p1)*...*(1-pn)
        if node.node_logic == DataDriven.Node_Logic.OR:
            for i in range(3):
                node.derived_score[i] = 1-node.derived_score[i]             # probability formula 2

        # next node(s)
        for next_node in node.next_node:
            Depth_First_Alg(node.derived_score, node.tolNumConditions, next_node)

def DerivedScore(leaf_queue):
    global LAG
    global derived_score_computation_time
    
    # starting timer for computation time
    start_time = time.time()
    
    # modifying derived scores
    while len(leaf_queue) > 0:
        node = leaf_queue.pop()
        for next_node in node.next_node:
            Depth_First_Alg(node.derived_score, 1, next_node)
    
    # calculating computation time
    derived_score_computation_time = time.time() - start_time
            

@data_analysis_bp.route('/data_driven/get_derived_scores', methods=['GET'])
def getDerivedScores():
    global LAG
    global derived_score_computation_time

    # converting to JSON
    node_type_to_str = {
        DataDriven.Node_Type.DERIVATION : 'Derivation', 
        DataDriven.Node_Type.DERIVED : 'Derived Fact',
        DataDriven.Node_Type.PRIMITIVE_FACT: 'Primitive Fact'}

    vertices = []
    edges = []
    for node in LAG: 
        vertices.append({
                'id' : node.index,
                'description' : node.description,
                'node_type' : node_type_to_str[node.node_type], 
                'base_score' : round(node.derived_score[0],3),
                'exploitability_score' : round(node.derived_score[1],3),
                'impact_score' : round(node.derived_score[2],3)})
        for e in node.next_node:
            edges.append({'source' : node.index, 'target' : e.index})
    
    return jsonify({'nodes': vertices, 'edges' : edges, "computation_time" : derived_score_computation_time})

#################### DATA-DRIVEN LAG Metrics ########################
@data_analysis_bp.route('/data_driven/percentage_execCode_nodes', methods=['GET'])
def percentage_execCode_nodes():
    global LAG
    sum = 0
    for node in LAG:
        sum += node.isExecCode

    result=round((float(sum) / float(len(LAG)) * 100.0),3)
    print(sum)
    return jsonify({'percentage_execCode_nodes': result})

# returns the execCode nodes with their probabilities
@data_analysis_bp.route('/data_driven/execCode_node_probabilities', methods=['GET'])
def execCode_node_probabilities():
    global LAG

    vertices = []
    for node in LAG: 
        if node.isExecCode:
            vertices.append({
                'id' : node,
                'description' : node.description,
                'node_type' : 'Derived Fact', 
                'base_score' : round(node.derived_score[0],3),
                'exploitability_score' : round(node.derived_score[1],3),
                'impact_score' : round(node.derived_score[2],3)})
    
    return jsonify({'nodes': vertices})

# returns the derived nodes with their probabilities
@data_analysis_bp.route('/data_driven/derived_node_probabilities', methods=['GET'])
def derived_node_probabilities():
    global LAG

    vertices = []
    for node in LAG: 
        if node.node_type == DataDriven.Node_Type.DERIVED:
            vertices.append({
                'id' : node,
                'description' : node.description,
                'node_type' : 'Derived Fact', 
                'base_score' : round(node.derived_score[0],3),
                'exploitability_score' : round(node.derived_score[1],3),
                'impact_score' : round(node.derived_score[2],3)})
    
    return jsonify({'nodes': vertices})

@data_analysis_bp.route('/data_driven/percentage_rule_nodes', methods=['GET'])
def percentage_rule_nodes():
    global LAG
    rules = 0
    for node in LAG:
        rules += (node.node_type == DataDriven.Node_Type.DERIVATION)

    result=round((float(rules) / float(len(LAG)) * 100.0),3)
    return jsonify({'percentage_rule_nodes': result})

@data_analysis_bp.route('/data_driven/percentage_derived_nodes', methods=['GET'])
def percentage_derived_nodes():
    global LAG
    numDerived = 0
    for node in LAG:
        numDerived += (node.node_type == DataDriven.Node_Type.DERIVED)
    
    result=round((float(numDerived) / float(len(LAG)) * 100.0),3)
    return jsonify({'percentage_derived_nodes': result})

@data_analysis_bp.route('/data_driven/network_entropy', methods=['GET'])
def network_entropy():
    global LAG
    net_entropy = [0.0,0.0,0.0]
    for node in LAG:
        for i in range(3):
            net_entropy[i] += node.derived_score[i] * math.log2(node.derived_score[i])
    
    for i in range(3):
        net_entropy[i] *= -1.0
        
    result = [] 
    result.append({'base' : round(net_entropy[0],3)})
    result.append({'exploitability' : round(net_entropy[1],3)})
    result.append({'impact' : round(net_entropy[2],3)})

    return jsonify({'network_entropy': result})

# 3.a
@data_analysis_bp.route('/data_driven/conditions_per_derived_node', methods=['GET'])
def conditions_per_derived_nodes():
    global LAG

    conditions_derived = []
    for node in LAG:
        if node.node_type == DataDriven.Node_Type.DERIVED:
            conditions_derived.append({
                "id" : node,
                "num_conditions" : node.tolNumConditions # total number of conditions to reach node
            })
    
    return jsonify({"conditions_per_derived_node" : conditions_derived})

# 3.c
@data_analysis_bp.route('/data_driven/conditions_per_execCode_node', methods=['GET'])
def conditions_per_execCode_node():
    global LAG

    conditions_derived = []
    for node in LAG:
        if node.isExecCode:
            conditions_derived.append({
                "id" : node,
                "num_conditions" : node.tolNumConditions # total number of conditions to reach node
            })
    
    return jsonify({"conditions_per_execCode_node" : conditions_derived})

# 3.d
@data_analysis_bp.route('/data_driven/rules_per_derived_node', methods=['GET'])
def rules_per_derived_nodes():
    global LAG

    rules_derived = []
    for node in LAG:
        if node.node_type == DataDriven.Node_Type.DERIVED:
            rules_derived.append({
                "id" : node,
                "num_conditions" : node.diNumConditions # direct number of rules
            })
    
    return jsonify({"rules_per_derived_node" : rules_derived})

# 3.e
@data_analysis_bp.route('/data_driven/rules_per_execCode_node', methods=['GET'])
def rules_per_execCode_node():
    global LAG

    rules_derived = []
    for node in LAG:
        if node.isExecCode:
            rules_derived.append({
                "id" : node,
                "num_conditions" : node.diNumConditions   # direct number of rules
            })
    
    return jsonify({"rules_per_execCode_node" : rules_derived})