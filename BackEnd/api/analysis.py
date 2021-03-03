from flask import Blueprint, jsonify, request
import enum
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
        derived_score = [1.0,1.0,1.0]   # base, exploitability, impact scores
        discription = str()             # node discription
        node_type = None                # type of node  
        node_logic = None               # node relationship 
        next_node = []                  # next nodes
        calculations_remaining = 0      # number of nodes needed to calculate derived score
        isExecCode = False              # whether node is execCode node (used for percentage execCode metric)


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
    while not leaf_queue.empty():
        node = leaf_queue.pop()
        for key in node.next_node:
            Depth_First_Alg(node.derived_score, key)
        
    return LAG

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
                'base_score' : LAG[key].derived_score[0],
                'exploitability_score' : LAG[key].derived_score[1],
                'impact_score' : LAG[key].derived_score[2]})
        for e in LAG[key].next_node:
            edges.append({'source' : key, 'target' : e})
    
    return jsonify({'nodes': vertices, 'edges' : edges})

################## MODEL DRIVEN ##############################
class ModelDriven:
    class Edge:
        weight = float()
        target = None
    class Node:
        edges = []          # array of edges
        discription = str() # node discription    