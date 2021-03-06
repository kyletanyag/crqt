'''
@author Thomas Laverghetta
@brief main executable for back-end. It has the job of initializating flask and databases. 

'''
from flask import Flask 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(__name__)
    CORS(app)
    
    # Configuring database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../dms/users.db' # setting database location for user-database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # for multiple databases (product and user databases)
    app.config['SQLALCHEMY_BINDS'] = {
        'users':     app.config['SQLALCHEMY_DATABASE_URI'],
        'products': 'sqlite:///../dms/products.db'
    }

    db.init_app(app)

    # # registering blueprints (routes)
    from .user_db import user_bp
    from .nvd import nvd_bp
    from .graph_generation import graph_bp
    from .data_driven_analysis import data_analysis_bp
    from .model_driven_analysis import model_analysis_bp
    from .products import product_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(nvd_bp)
    app.register_blueprint(graph_bp)
    app.register_blueprint(data_analysis_bp)
    app.register_blueprint(model_analysis_bp)
    app.register_blueprint(product_bp)

    return app