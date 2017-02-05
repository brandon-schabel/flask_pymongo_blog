from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, current_user,logout_user

''' Response, jsonify, make_response, url_for, render_template, \
    send_from_directory, request, url_for, redirect, flash, Blueprint
from flask_bootstrap import Bootstrap
from pymongo import MongoClient, DESCENDING, IndexModel, TEXT
from datetime import datetime, timedelta
from blueprints.db_config import *
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from bson.objectid import ObjectId
'''
from blueprints.sec_key import *


app = Flask(__name__)
bcrypt = Bcrypt(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.loging_view = 'login'

from blueprints.login.routes import mod
from blueprints.site.routes import mod

app.register_blueprint(login.routes.mod, url_prefix='/login')
app.register_blueprint(site.routes.mod)

app.config.update(SECRET_KEY=sec_key)