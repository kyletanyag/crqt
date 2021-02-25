from flask import Blueprint, jsonify, request
from . import db 
from .nvd import CVSS

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

# graph data structure (adjenency list)
class Node:
    derived_score = [1.0,1.0,1.0]   # base, exploitability, impact scores
    node_type = Node_Type(0)        # type of node  
    node_logic = Node_Logic(0)      # node relationship 
    next_node = []                  # next nodes


'''
Probability Formulas:
For any n events e1, e2, ..., en:
	P(e1, e2, ..., en)=product(P(ei),1,n)				// product (expression, lower, upper)
	P(e1 U e2 U ... U en) = 1 - product(P(NOT(ei)),1,n)		// http://people.duke.edu/~hpgavin/cee201/ProbabilityRules.pdf
'''


LAG = {}
def Depth_First_Search(scores, key):
    global LAG

    # modifying score
    if LAG[key].node_logic == Node_Logic.OR:
        # OR = (1-p1)*...*(1-pn)
        for i in range(3):
            LAG[key].derived_score[i] = LAG[key].derived_score[i]*(1-scores[i]) 
    else: # node_log == AND
        # AND = p1*...*pn
        for i in range(3):
            LAG[key].derived_score[i] = LAG[key].derived_score[i]*scores[i] 
    
    # next node
    for k in LAG[key].next_node:
        Depth_First_Search(scores, k)
    


def DerivedScore(lag_dict, leaf_queue):
    global LAG
    LAG = lag_dict
    
    # modifying derived scores
    while not leaf_queue.empty():
        node = leaf_queue.pop()
        for key in node.next_node:
            Depth_First_Search(node.derived_score, key)
    
    # finalize scores (Finish modifying OR)
    for key in LAG:
        if LAG[key].node_logic == Node_Logic.OR:
            for i in range(3):
                LAG[key].derived_score[i] = 1-LAG[key].derived_score[i] 
    
    return LAG
    