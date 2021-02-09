from flask import Blueprint, jsonify, request
from . import db 

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/verify_user', methods=['POST'])
def verify_user():
    request.get_json()
    ## query with MySQL
    # IF USERNAME FOUND: THEN 
    # - COMPARE PASSWORDS (HASH GIVEN PASSWORD)
    # - IF PASSWORDS ARE EQUIVLENT:
    # -- RETRUN TRUE
    # 
    # RETURN FALSE

    # username=key, password, email
    # Python Hash function: https://docs.python.org/3/library/hashlib.html (open-source)

@user_bp.route('/register', methods=['POST'])
def register():
    request.get_json() # who (name, email, organization), why (why they need access)
    # send msg to admins 

# admin call ONLY
@user_bp.route('/add_user_init', methods=['POST'])
def add_user_init():
    request.get_json() # who (name, email, organization), why (why they need access)
    # send msg to user

@user_bp.route('/add_user', methods=['POST'])
def add_user():
    request.get_json() # 
    # send msg to user
