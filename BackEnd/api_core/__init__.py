'''
@author Thomas Laverghetta
@brief This is implementation of a simple Flask and React tutorial I found on Youtube. 

'''
from flask import Flask 
from flask_cors import CORS
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="testdb"
)

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    from .views import main
    app.register_blueprint(main)

    return app