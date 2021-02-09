from flask import Blueprint, jsonify, request
from . import db 

nvd_bp = Blueprint('nvd_bp', __name__)