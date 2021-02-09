'''
@author Thomas Laverghetta
@brief This is the logical attack graph (LAG) generation module. It will accept csv files from front-end which contain vertices and edges for user provided network. 

'''
from flask import Blueprint, jsonify, request
from . import db 
import .nvd

# route for LAG generation module
graph_bp = Blueprint('graph_bp', __name__)
