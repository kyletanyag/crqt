'''
@author Thomas J. Laverghetta
@brief Contains all functions for analyzing data-driven inputs.
These include:
- Derived Score
- %execCode
- %rule
- network entropy
- node condition statistics

'''

from round_sig import round_sig
from enum import Enum, auto
from copy import deepcopy 
from collections import deque
import math
import requests
import time
import numpy as np

# Global Var
LAG = []                                # holds network topology
derived_score_computation_time = 0.0    # computation time for derived score calculation
HAS_DERIVED_SCORE_CALC = False          # bool for whether derived score has been computed
LEAF_QUEUE = deque()                    # queue for leaf nodes in network for derived score computation

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
            self.derived_score = np.array([1.0,1.0,1.0])   # base, exploitability, impact scores
            self.description = discription          # node description
            self.node_type = None                   # type of node  
            self.node_logic = DataDriven.switch[logic]# node relationship 
            self.next_node = []                     # next nodes
            self.calculations_remaining = 0         # number of nodes needed to calculate derived score
            self.isExecCode = False                 # whether node is execCode node (used for percentage execCode metric)
            self.tolNumConditions = 0               # total num of conditions to reach node
            self.tolNumRules = 0                    # number of rules to reach node

        def printFunc(self):
            print(self.derived_score, self.description, self.node_type, self.node_logic, self.next_node, self.calculations_remaining, self.isExecCode)

# resetting global variables
def DataDriven_init():
    global LAG
    global derived_score_computation_time
    global HAS_DERIVED_SCORE_CALC
    global LEAF_QUEUE

    HAS_DERIVED_SCORE_CALC = False
    LEAF_QUEUE = deque()
    LAG.clear()
    derived_score_computation_time = 0.0

'''
Probability Formulas:
For any n events e1, e2, ..., en:
	1. P(e1, e2, ..., en)=product(P(ei),1,n)				    // product (expression, lower, upper)
	2. P(e1 U e2 U ... U en) = 1 - product(P(NOT(ei)),1,n)		// http://people.duke.edu/~hpgavin/cee201/ProbabilityRules.pdf
'''

# supports derived score function by calculating derived score of all nodes
# Algorithm works by working out to in. First leaf nodes add their score to corresponding rule nodes.
# After addition of score, rule node will determine if all leaf nodes have added their scores. If not, 
# then it will end function call and wait for all leaf nodes to add their score. If all leaf nodes have add their score,
# then rule node will add score to node(s) it is pointing at, and the process continues in this pattern. 
# node will determine if all previous nodes have added their score to it; if so, adds score to 
# node(s) its pointing too; else, will end function call and wait until all nodes have added their scores
def Depth_First_Alg(scores, tolNumConditions, tolNumRules, node): 
    # reduce number of nodes needed to make calculation
    node.calculations_remaining -= 1
    
    # adding number of conditions to reach node
    node.tolNumConditions += tolNumConditions
    node.tolNumRules += tolNumRules

    # modifying score
    if node.node_logic == DataDriven.Node_Logic.OR:
        # OR = (1-p1)*...*(1-pn)
        node.derived_score *= (1-scores)     # probability formula 2
    else: # node_log == AND OR FLOW
        # AND = p1*...*pn
        node.derived_score *= scores         # probability formula 1
      
    # if no more nodes are required to make calculation
    if node.calculations_remaining == 0:
        # if OR node, then finalize calculation
        # 1 - (1-p1)*...*(1-pn)
        if node.node_logic == DataDriven.Node_Logic.OR:
            node.derived_score = 1-node.derived_score             # probability formula 2

        # if rule node, increment number of rules
        if node.node_type == DataDriven.Node_Type.DERIVATION:
            node.tolNumRules += 1

        # next node(s)
        for next_node in node.next_node:
            Depth_First_Alg(node.derived_score, node.tolNumConditions, node.tolNumRules, next_node)

# computes derived scores for all nodes using exploitability, impact, and base scores
# leaf_queue is queue of leaf nodes found in graph generation module
def DerivedScore():
    global LAG
    global derived_score_computation_time
    global HAS_DERIVED_SCORE_CALC
    global LEAF_QUEUE

    if (not HAS_DERIVED_SCORE_CALC):
        # starting timer for computation time
        start_time = time.time()
        
        # modifying derived scores
        while len(LEAF_QUEUE) > 0:
            node = LEAF_QUEUE.pop()
            for next_node in node.next_node:
                # derived score, #conditions, #rules, next_nodes[]
                Depth_First_Alg(node.derived_score, 1, 0, next_node)
        
        # calculating computation time
        derived_score_computation_time = time.time() - start_time

        HAS_DERIVED_SCORE_CALC = True

    # converting to JSON
    node_type_to_str = {
        DataDriven.Node_Type.DERIVATION : 'Derivation', 
        DataDriven.Node_Type.DERIVED : 'Derived Fact',
        DataDriven.Node_Type.PRIMITIVE_FACT: 'Primitive Fact'
    }

    vertices = []
    edges = []
    for node in LAG: 
        vertices.append({
            'id' : node.index,
            'description' : node.description,
            'node_type' : node_type_to_str[node.node_type], 
            'base_score' : round_sig(node.derived_score[0],3),
            'exploitability_score' : round_sig(node.derived_score[1],3),
            'impact_score' : round_sig(node.derived_score[2],3)
        })
    
    return {'nodes': vertices, "computation_time" : derived_score_computation_time}

#################### DATA-DRIVEN LAG Metrics ########################
# returns percentage of execCode nodes
def percentage_execCode_nodes():
    global LAG
    result = float(sum(node.isExecCode for node in LAG)) / float(len(LAG)) * 100.0
    return {'percentage_execCode_nodes': round_sig(result,3)}

# returns the execCode nodes with their probabilities
def execCode_node_probabilities():
    global LAG

    vertices = []
    for node in LAG: 
        if node.isExecCode:
            vertices.append({
                'id' : node.index,
                'description' : node.description,
                'node_type' : 'Derived Fact', 
                'base_score' : round_sig(node.derived_score[0],3),
                'exploitability_score' : round_sig(node.derived_score[1],3),
                'impact_score' : round_sig(node.derived_score[2],3)
            })
    
    return {'nodes': vertices}

# returns the derived nodes with their probabilities
def derived_node_probabilities():
    global LAG

    vertices = []
    for node in LAG: 
        if node.node_type == DataDriven.Node_Type.DERIVED:
            vertices.append({
                'id' : node.index,
                'description' : node.description,
                'node_type' : 'Derived Fact', 
                'base_score' : round_sig(node.derived_score[0],3),
                'exploitability_score' : round_sig(node.derived_score[1],3),
                'impact_score' : round_sig(node.derived_score[2],3)
            })
    
    return {'nodes': vertices}

# returns percentage of rule nodes
def percentage_rule_nodes():
    global LAG
    result = float(sum(node.node_type == DataDriven.Node_Type.DERIVATION for node in LAG)) / float(len(LAG)) * 100.0
    return {'percentage_rule_nodes': round_sig(result,3)}

# returns percentage of derived nodes
def percentage_derived_nodes():
    global LAG
    result=(float(sum(node.node_type == DataDriven.Node_Type.DERIVED for node in LAG)) / float(len(LAG)) * 100.0)  
    return ({'percentage_derived_nodes': round_sig(result,3)})

# returns network entropy calculation
def network_entropy():
    global LAG
    net_entropy = np.sum([node.derived_score * np.log2(node.derived_score) for node in LAG], axis=0)
    net_entropy *= -1.0
    
    return ({
        'network_entropy': [
                {'base' : round_sig(net_entropy[0],3)},
                {'exploitability' : round_sig(net_entropy[1],3)},
                {'impact' : round_sig(net_entropy[2],3)}
            ]
        })

# returns the number of conditions per derived node
def conditions_per_derived_nodes():
    global LAG

    conditions_derived = []
    for node in LAG:
        if node.node_type == DataDriven.Node_Type.DERIVED:
            conditions_derived.append({
                "id" : node.index,
                "description": node.description,
                "num_conditions" : node.tolNumConditions # total number of conditions to reach node
            })
    
    return {"conditions_per_derived_node" : conditions_derived}, 200

# returns the number of conditions per execCode node
def conditions_per_execCode_node():
    global LAG

    conditions_derived = []
    for node in LAG:
        if node.isExecCode:
            conditions_derived.append({
                "id" : node.index,
                "description": node.description,
                "num_conditions" : node.tolNumConditions # total number of conditions to reach node
            })
    
    return {"conditions_per_execCode_node" : conditions_derived}, 200

# returns the number of rules per derived node
def rules_per_derived_nodes():
    global LAG

    rules_derived = []
    for node in LAG:
        if node.node_type == DataDriven.Node_Type.DERIVED:
            rules_derived.append({
                "id" : node.index,
                "description": node.description,
                "num_rules" : node.tolNumRules  # number of rules
            })
    
    return {"rules_per_derived_node" : rules_derived}, 200

# returns the number of rules per execCode node
def rules_per_execCode_node():
    global LAG

    rules_derived = []
    for node in LAG:
        if node.isExecCode:
            rules_derived.append({
                "id" : node.index,
                "description": node.description,
                "num_rules" : node.tolNumRules   # num of rules
            })
    
    return {"rules_per_execCode_node" : rules_derived}, 200

# returns the number of conditions and rules per node
def conditions_and_rules_per_nodde():
    global LAG

    derived = []
    for node in LAG:
        if node.node_type == DataDriven.Node_Type.DERIVED:
            derived.append({
                "id" : node.index,
                "description": node.description,
                "num_conditions": node.tolNumConditions,
                "num_rules" : node.tolNumRules # direct number of rules
            })
    return {"derived_data": derived}, 200