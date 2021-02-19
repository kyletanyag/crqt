'''
@author Thomas Laverghetta
@brief this file contains processes to communicate with user-database. 

'''
from flask import Blueprint, jsonify, request
import hashlib

from sqlalchemy.orm.session import Session
from . import db 
from .data_models import User_Role
from .data_models import Users
import os
import io
import base64
import onetimepass as otp
import enum
import pyqrcode

user_bp = Blueprint('user_bp', __name__)

# route to verify username and password
@user_bp.route('/verify_user')
def verify_user():
    # query with SQL given user_info.username
    user = request.get_json()  # username and passwd
    user_db_entry = Users.query.filter_by(username=user['username']).first()

    if user['username'] == user_db_entry.username:
        print ("User found.")
        u_hash = hashlib.sha256()
        u_hash.update(user['password'].encode())
        password = str(u_hash.digest())

        if password == user_db_entry.password:
            print ("Password match.")
            return 'Passwords Match', 201
        else:
            print ("Password does not match.")
        return 'Passwords Do Not Match', 201 

    print ("User not found.")
    return 'User not found', 404

# get 2FA 6-digit pin 
@user_bp.route('/otp/<user_i>')
def get_otp(user_i):
    user_db_entry = Users.query.filter_by(username=user_i).first()

    if user_db_entry is not None:

        return str(otp.get_totp(user_db_entry.otp_secret)), 201
    else:
        return 'Cannot generate token', 201

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
    user_db_entry = Users.query.filter_by(username=user['username']).first()

    if False if user_db_entry is None else user['username'] == user_db_entry.username:
        print ("Username already exists.  Please select a new username.")
        return 'Done'

    else:
        hash = hashlib.sha256()
        hash.update(user['password'].encode())
        password_hash = str(hash.digest())
        secret = base64.b32encode(os.urandom(10)).decode('utf-8')

        # new_user = Users(username=user['username'], password=password_hash, 
        #     first_name=user['first_name'], last_name=user['last_name'], 
        #     email=user['email'], user_role=user['user_role'], 
        #     is_registered=False, otp_secret=secret)

        new_user = Users(username=user['username'], password=password_hash, 
            first_name=user['first_name'], last_name=user['last_name'], 
            email=user['email'], user_role=user['user_role'], 
            is_registered=False, otp_secret=secret)

        db.session.add(new_user)
        db.session.commit()

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
        'There is no username matching {}'.format(Users.username))

    url = pyqrcode.create(f'otpauth://totp/CRQT:{user_db_entry.username}?secret={user_db_entry.otp_secret}&issuer=CRQT')

    stream = io.BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'img/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
        }
