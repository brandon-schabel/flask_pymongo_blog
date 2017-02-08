from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, current_user,logout_user
import flask.globals as flask_global
from blueprints.User import User
'''
how to get user_loader working accross apps
http://stackoverflow.com/questions/20136090/how-do-i-handle-login-in-flask-with-multiple-blueprints?noredirect=1&lq=1
'''
from blueprints.db_config import *

app = Flask(__name__)
bcrypt = Bcrypt(app)
Bootstrap(app)

login_manager = LoginManager()
#login_manager.init_app(app)
login_manager.setup_app(app)
login_manager.loging_view = 'login'

from blueprints.login.routes import mod
from blueprints.site.routes import mod

app.register_blueprint(login.routes.mod, url_prefix='/login')
app.register_blueprint(site.routes.mod)

app.config.update(SECRET_KEY=sec_key)

@login_manager.user_loader
def load_user(username):  
    u = user_coll.find_one({"username": username})
    if not u:
        return None
    
    '''blueprint = flask_global.current_app.blueprints[request.blueprint]

    if hasattr(Blueprint, load_user):'''
    return User(u['username'])