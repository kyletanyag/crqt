'''
@author Thomas Laverghetta
@brief main executable for back-end. It has the job of initializating flask and databases. 

'''
from flask import Flask 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuring database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../dms/users.db' # setting database location for user-database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # for multiple databases
    app.config['SQLALCHEMY_BINDS'] = {
        'users':     app.config['SQLALCHEMY_DATABASE_URI'],
        'nvd':      'sqlite:///../dms/nvd.db'
    }

    db.init_app(app)

    # # registering blueprints (routes)
    # from .user_db import user_bp
    # from .nvd import nvd_bp
    # from .graph_generation import graph_bp
    # app.register_blueprint(user_bp)
    # app.register_blueprint(nvd_bp)
    # app.register_blueprint(graph_bp)
    
    return app

