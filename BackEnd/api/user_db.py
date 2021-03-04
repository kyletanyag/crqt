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

# route to verify email and password
@user_bp.route('/verify_user')
def verify_user():
    # query with SQL given user_info.eail
    user = request.get_json()  # email and password
    user_db_entry = Users.query.filter_by(username=user['email']).first()

    if user['email'] == user_db_entry.email:
        print ("User found.")
        u_hash = hashlib.sha256()
        u_hash.update(user['password'].encode())
        password = str(u_hash.digest())

        if password == user_db_entry.password:
            print ("Password match.")
            return {'message': 'Passwords Match.', 
                    '2fa': user_db_entry.enabled_2fa}, 201
        else:
            print ("Password does not match.")
        return 'Passwords Do Not Match', 201 

    print ("User not found.")
    return 'User not found', 404

# route to verify otp
@user_bp.route('/verify_otp')
def get_otp():
    user = request.get_json()
    user_db_entry = Users.query.filter_by(email=user['email']).first()

    if user_db_entry is not None:
        return {'access' : str(otp.get_totp(user_db_entry.otp_secret)) == user['pin']}, 200
    else:
        return 'Cannot generate token', 201


# user registration route
@user_bp.route('/register', methods=['POST'])
def register():
    user = request.get_json() # who (name, email, organization), why (why they need access)
    
    # query with SQL given user_info.username
    user_db_entry = Users.query.filter_by(email=user['email']).first()

    if False if user_db_entry is None else user['email'] == user_db_entry.email:
        return {'error': 'Account with associated email already exists.'}, 200

    else:
        hash = hashlib.sha256()
        hash.update(user['password'].encode())
        password_hash = str(hash.digest())
        secret = base64.b32encode(os.urandom(10)).decode('utf-8')

        # new_user = Users(username=user['username'], password=password_hash, 
        #     first_name=user['first_name'], last_name=user['last_name'], 
        #     email=user['email'], user_role=user['user_role'], 
        #     is_registered=False, otp_secret=secret)

        new_user = Users(email=user['email'], password=password_hash, 
            first_name=user['first_name'], last_name=user['last_name'], 
            user_role=user['user_role'], is_registered=False, otp_secret=secret, 
            enabled_2fa=False)

        db.session.add(new_user)
        db.session.commit()

        return 'Done', 201

    # Send email/msg to admin about registration of user


# Admin adds user to accepted list of registration. admin call ONLY
@user_bp.route('/approve_user/<input>')
def approve_user(input):
    user = Users.query.filter_by(id=input).first_or_404(description=
        'Account not found.')

    user.is_registered = True
    db.session.commit()

    return 'Done', 200

# Admin deletes a user's account
@user_bp.route('/delete_user/<input>')
def delete_user(input):
    user = Users.query.filter_by(id=input).first_or_404(description=
        'Account not found.')

    db.session.delete(user)
    db.session.commit()

    return 'Done', 200



# returns a json file containing a collection of users that are registered 
@user_bp.route('/get_registered_users')
def get_registered_users():

    # query with SQL for all contents
    user_list = Users.query.all()
    registered_users = []

    for n in user_list:
        if n.is_registered == True:
            registered_users.append({
                'email' : n.email, 
                'id' : n.id,
                'name' : n.first_name + ' ' + n.last_name,
                'role' : 'Admin' if n.user_role == 1 else 'Common', 
                'is_registered' : n.is_registered})
    
    return jsonify({'registered_users' : registered_users}), 200


# returns a json file containing a collection of users that are NOT registered 
@user_bp.route('/get_unregistered_users')
def get_unregistered_users():

    # query with SQL for all contents
    user_list = Users.query.all()
    unregistered_users = []

    for n in user_list:
        if n.is_registered == False:
            unregistered_users.append({
                'email' : n.email, 
                'id' : n.id,
                'name' : n.first_name + ' ' + n.last_name, 
                'role' : 'Admin' if n.user_role == 1 else 'Common', 
                'is_registered' : n.is_registered})
    
    return jsonify({'unregistered_users': unregistered_users}), 200

@user_bp.route('/qrcode/<input>')
def qrcode(input):
    user_db_entry = Users.query.filter_by(id=input).first_or_404(description=
        'There is no matching account with the email: {}'.format(Users.email))

    url = pyqrcode.create(f'otpauth://totp/CRQT:{user_db_entry.email}?secret={user_db_entry.otp_secret}&issuer=CRQT')

    stream = io.BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'img/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
        }
