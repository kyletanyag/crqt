'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with user-database. 

'''
from flask import Blueprint, jsonify, request
import hashlib
from . import db 

user_bp = Blueprint('user_bp', __name__)

# user verification route
@user_bp.route('/verify_user')
def verify_user():
    user = request.get_json()  # username and passwd
    # query with SQL given user_info.username
    user_list = Users.query.all()

    for n in user_list:
        if user.username == n.username:
            print ("User found.")
            u_hash = hashlib.sha256()
            n_hash = hashlib.sha256()
            u_hash.update(user.password)
            n_hash.update(n.password)

            if u_hash.digest() == n_hash.digest():
                print ("Password match.")
                return True
            else:
                print ("Password does not match.")
                return False
    

    print ("User not found.")
    return False



    # IF USERNAME FOUND IN QUERY: THEN 
    # - COMPARE PASSWORDS (HASH GIVEN PASSWORD)
    # - IF PASSWORDS ARE EQUIVLENT:
    # -- RETRUN TRUE
    # 
    # RETURN FALSE

    # username=key, password, email
    # Python Hash function: https://docs.python.org/3/library/hashlib.html (open-source)

# user registration route
@user_bp.route('/register', methods=['POST'])
def register():
    user = request.get_json() # who (name, email, organization), why (why they need access)
    
    # Send email/msg to admin about registration of user

# Admin adds user to accepted list of registration. admin call ONLY
@user_bp.route('/add_user_init', methods=['POST'])
def add_user_init():
    user = request.get_json() # who (name, email, organization), why (why they need access)
    
    # Send email/msg to user with link to add_user route so they can put in their crodentials

# 
@user_bp.route('/add_user', methods=['POST'])
def add_user():
    user = request.get_json()
    
    # Insert user info into SQL
