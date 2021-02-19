'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with user-database. 

'''
from flask import Blueprint, jsonify, request
import hashlib
from . import db 
from .data_models import User_Role
from .data_models import Users
import os
import io
import base64
import onetimepass
import enum
import pyqrcode

user_bp = Blueprint('user_bp', __name__)

# route to verify username and password
@user_bp.route('/verify_user')
def verify_user():
    # query with SQL given user_info.username
    user = request.get_json()  # username and passwd
    user_db_entry = Users.query.filter_by(username=user.username).first_or_404(description=
        'There is no username to verify: {}'.format(Users.username))

    if user['username']== user_db_entry.username:
        print ("User found.")
        u_hash = hashlib.sha256()
        u_hash.update(user['password'])

        if u_hash.digest() == user_db_entry.password:
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
    
    # query with SQL given user_info.username
    user_db_entry = Users.query.filter_by(username=user['username']).first_or_404(description=
        'There is no username: {}'.format(user['username']))

    if user_db_entry is None:
        return False, 201

    elif user['username'] == user_db_entry.username:
        print ("Username already exists.  Please select a new username.")
        return 'Done'

    else:
        password_hash = hashlib.sha256()
        password_hash.update(user['password'])
        
        secret = base64.b32encode(os.urandom(10)).decode('utf-8')

        new_user = Users(username=user['username'], password=password_hash.digest(), 
            first_name=user['first_name'], last_name=user['last_name'], 
            email=user['email'], user_role=user['user_role'], 
            is_registered=False, otp_secret=secret)

        db.session.add(new_user)
        db.session.commmit()

        return 'Done', 201

    # Send email/msg to admin about registration of user

# Admin adds user to accepted list of registration. admin call ONLY
@user_bp.route('/add_user_init', methods=['POST'])
def add_user_init():

    # who (name, email, organization), why (why they need access)
    # may need revising once we determine what data is passed
    user = request.get_json() 
    
    # query with SQL given user_info.username
    user_list = Users.query.all()

    # searches for the user by username, then changes the is_registered variable to true
    for n in user_list:
        if user.username == n.username:
            entry = Users.query.filter_by(username=user.username).first()
            entry.is_registered = True
            db.session.commmit()
            print ("User :", user.username, ", is now registered.")
            return 'Done'
    
    # if the for loop completes, it is assumed that the username did not exist in the db
    print ("User :", user.username, ", was not found.")
    return 'Done'
    # Send email/msg to user with link to add_user route so they can put in their crodentials

# returns a json file containing a collection of users that are registered 
@user_bp.route('/get_registered_users')
def get_registered_users():

    # query with SQL for all contents
    user_list = Users.query.all()
    verified_users = []

    for n in user_list:
        if n.username == True:
            verified_users.append({'username' : n.username, 'password' : n.password, 
            'first_name' : n.first_name, 'last_name' : n.last_name, 'email' : n.email, 
            'user_role' : n.user_role, 'is_registered' : n.is_registered, 'auth_key' : n.auth_key})
    
    return jsonify({'verified_users' : verified_users})


# returns a json file containing a collection of users that are NOT registered 
@user_bp.route('/get_unregistered_users')
def get_unregistered_users():

    # query with SQL for all contents
    user_list = Users.query.all()
    verified_users = []

    for n in user_list:
        if n.username == True:
            verified_users.append({'username' : n.username, 'password' : n.password, 
            'first_name' : n.first_name, 'last_name' : n.last_name, 'email' : n.email, 
            'user_role' : n.user_role, 'is_registered' : n.is_registered, 'auth_key' : n.auth_key})
    
    return jsonify({'verified_users' : verified_users})

@user_bp.route('/qrcode/<user_i>')
def qrcode(user_i):
    user_db_entry = Users.query.filter_by(username=user_i).first_or_404(description=
        'There is no username to verify: {}'.format(Users.username))

    url = pyqrcode.create(f'otpauth://totp/2FA-Demo:{user_db_entry.username}?secret={user_db_entry.otp_secret}&issuer=CRQT')

    stream = io.BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'img/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
        }
