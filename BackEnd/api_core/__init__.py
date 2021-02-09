'''
@author Thomas Laverghetta
@brief This is implementation of a simple Flask and React tutorial I found on Youtube. 

'''
from flask import Flask 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../dms/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
'users':     app.config['SQLALCHEMY_DATABASE_URI'],
'nvd':      'sqlite:///../dms/nvd.db'
}

# registering blueprints
from .user_db import user_bp
from .nvd import nvd_bp
app.register_blueprint(user_hp)
app.register_blueprint(nvd_bp)


if __name__ == "__main__":
    app.run()