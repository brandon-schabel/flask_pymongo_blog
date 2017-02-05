from flask import Response, Flask, jsonify, make_response, url_for, render_template, \
    send_from_directory, request, url_for, redirect, flash, Blueprint
from flask_login import LoginManager, login_required, login_user, current_user,logout_user
from flask_bootstrap import Bootstrap
from pymongo import MongoClient, DESCENDING, IndexModel, TEXT
from datetime import datetime, timedelta
from blueprints.site.db_config import *
#from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from blueprints.site.forms import NewPostForm
from bson.objectid import ObjectId
from blueprints.login.routes import mod
from blueprints.site.User import User
from pymongo import MongoClient
from blueprints.site.login_config import *

#from blueprints.login.routes import mod
#app.register_blueprint(login.routes.mod, url_prefix='/login')
mod = Blueprint('site',__name__, template_folder= 'templates')

login_manager = LoginManager()
client = MongoClient(server_url)
db = client[db_server_name]
db.authenticate(db_user, db_pass)
user_coll = db[user_collection]
post_coll = db[post_collection]
#login_manager.init_app(mod)
#login_manager.loging_view = 'login'



@mod.record_once
def on_load(state):
    login_manager.init_app(state.app)

@login_manager.user_loader
def load_user(username):  
    u = user_coll.find_one({"username": username})
    if not u:
        return None
    
    '''blueprint = flask_global.current_app.blueprints[request.blueprint]

    if hasattr(Blueprint, load_user):'''
    return User(u['username'])

@mod.route('/')
def index():
    return render_template('site/index.html')


@mod.route("/newpost", methods=['GET', 'POST'])
@login_required
def newpost():
    form = NewPostForm(request.form)
    if request.method == 'POST' and form.validate():

        username = current_user.get_id()
        post_title = form.post_title.data
        post_content = form.post_content.data

        post_coll.insert(
            {'username': username, 'post_title': post_title, 'post_content': post_content})

        return redirect(url_for('site.index'))
    return render_template('site/newpost.html', form=form)


@mod.route("/viewpost")
@login_required
def viewpost():
    all_post = []
    for post in post_coll.find():
        all_post.append(post)

    return render_template('site/viewpost.html', all_post=all_post)
