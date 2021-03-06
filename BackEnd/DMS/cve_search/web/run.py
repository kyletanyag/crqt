import logging
import random
import urllib
from datetime import timedelta

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_breadcrumbs import Breadcrumbs
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS

from lib.Authentication import AuthenticationHandler
from lib.Config import Configuration
from lib.DatabaseSchemaChecker import SchemaChecker, DatabaseSchemaError
from lib.LogHandler import AppLogger
from lib.Toolkit import isURL
from lib.User import User

auth_handler = AuthenticationHandler()

logging.setLoggerClass(AppLogger)

login_manager = LoginManager()

app = None
token_blacklist = None
socketio = None

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)


def create_app(version, run_path):

    global app, token_blacklist, socketio

    app = Flask(__name__)
    CORS(app)

    app.config["version"] = version
    app.config["run_path"] = run_path

    config = Configuration()

    if config.getWebInterface().lower() == "full":
        app.config["WebInterface"] = False
    else:
        app.config["WebInterface"] = True

    app.config["MONGO_DBNAME"] = config.getMongoDB()
    app.config["SECRET_KEY"] = str(random.getrandbits(256))
    app.config["JWT_SECRET_KEY"] = str(random.getrandbits(256))

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = REFRESH_EXPIRES
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

    token_blacklist = config.getRedisTokenConnection()

    app.config["RESTX_MASK_SWAGGER"] = False

    socketio = SocketIO(app)

    Breadcrumbs(app=app)
    Bootstrap(app)
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):

        return {"user": identity}

    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        jti = decrypted_token["jti"]
        entry = token_blacklist.get(jti)
        if entry == "true":
            return True
        return False

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page!!!"
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(id):
        return User.get(id, auth_handler)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint)

    from .plugins import plugins as plugins_blueprint

    app.register_blueprint(plugins_blueprint, url_prefix="/plugin")

    if not app.config["WebInterface"]:
        from .auth import auth as auth_blueprint

        app.register_blueprint(auth_blueprint)

        from .admin import admin as admin_blueprint

        app.register_blueprint(admin_blueprint, url_prefix="/admin")

    from .restapi import blueprint as api

    app.register_blueprint(api)

    from .restapidocs import docs as docs_blueprint

    app.register_blueprint(docs_blueprint)

    @app.context_processor
    def version():
        def get_version():
            return app.config["version"]

        return dict(get_version=get_version)

    @app.context_processor
    def db_schema():
        def db_schema():
            sc = SchemaChecker()
            try:
                return sc.validate_schema()
            except DatabaseSchemaError as err:
                return err

        return dict(db_schema=db_schema)

    @app.context_processor
    def WebInterface():
        def get_WebInterface():
            return app.config["WebInterface"]

        return dict(get_WebInterface=get_WebInterface)

    @app.context_processor
    def JSON2HTMLTable():
        # Doublequote, because we have to |safe the content for the tags
        def doublequote(data):
            return urllib.parse.quote_plus(urllib.parse.quote_plus(data))

        def JSON2HTMLTableFilter(data, stack=None):
            _return = ""
            if type(stack) == str:
                stack = [stack]

            if type(data) == list:
                if len(data) == 1:
                    _return += JSON2HTMLTableFilter(data[0], stack)
                else:
                    _return += '<ul class="via4">'
                    for item in data:
                        _return += "<li>%s</li>" % JSON2HTMLTableFilter(item, stack)
                    _return += "</ul>"
            elif type(data) == dict:
                _return += '<table class="invisiTable">'
                for key, val in sorted(data.items()):
                    _return += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (
                        key,
                        JSON2HTMLTableFilter(val, stack + [key]),
                    )
                _return += "</table>"
            elif type(data) == str:
                if stack:
                    _return += (
                        "<a href='/link/"
                        + doublequote(".".join(stack))
                        + "/"
                        + doublequote(data)
                        + "'>"
                    )  # link opening
                    _return += "<i class='fas fa-link' aria-hidden='true'></i> </a>"
                _return += (
                    "<a target='_blank' href='%s'>%s</a>" % (data, data)
                    if isURL(data)
                    else data
                )
            _return += ""
            return _return

        return dict(JSON2HTMLTable=JSON2HTMLTableFilter)

    @app.template_filter("htmlEncode")
    def htmlEncode(string):
        return urllib.parse.quote_plus(string).lower()

    @app.template_filter("htmlDecode")
    def htmlDecode(string):
        return urllib.parse.unquote_plus(string)

    @app.template_filter("sortIntLikeStr")
    def sortIntLikeStr(datalist):
        return sorted(datalist, key=lambda k: int(k))

    @app.errorhandler(404)
    def page_not_found(error):
        return (
            render_template("404.html",),
            404,
        )

    return app, socketio
