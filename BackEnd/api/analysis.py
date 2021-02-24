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
    derived_score = [-1.0,-1.0,-1.0]# base, exploitability, impact scores
    node_type = Node_Type(0)        # type of node // need to fix -- kbt 
    node_logic = Node_Logic(0)      # node relationship // need to fix -- kbt
    next_node = []                  # next nodes

class PrimitiveFactNode():
    index = int()
    cvss_score = CVSS()
    next_node = []                  # next nodes


def DerivedScore(lag_dict, leaf_queue):
    pass