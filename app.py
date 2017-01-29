from flask import Response, Flask, jsonify, make_response, url_for, render_template, \
    send_from_directory, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from pymongo import MongoClient, DESCENDING, IndexModel, TEXT
from datetime import datetime, timedelta
import os
from app_config import *
from flask_login import LoginManager, login_required, login_user, current_user,logout_user
from User import User
from bson.objectid import ObjectId

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.loging_view = 'login'
Bootstrap(app)
bcrypt = Bcrypt(app)

app.config.update(SECRET_KEY= update_sec_key())