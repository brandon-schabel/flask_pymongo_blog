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
from forms import LoginForm, RegistrationForm, NewPostForm
from bson.objectid import ObjectId

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.loging_view = 'login'
Bootstrap(app)
bcrypt = Bcrypt(app)

from blueprints.login.routes import mod
app.register_blueprint(login.routes.mod)

app.config.update(SECRET_KEY= update_sec_key())

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/newpost", methods=['GET', 'POST'])
@login_required
def newpost():
    form = NewPostForm(request.form)
    if request.method == 'POST' and form.validate():

        username = current_user.get_id()
        post_title = form.post_title.data
        post_content = form.post_content.data

        post_coll.insert({'username':username, 'post_title':post_title, 'post_content': post_content})

        redirect(url_for('index'))
    return render_template('newpost.html', form=form)

@app.route("/viewpost")
@login_required
def viewpost():
    all_post = []
    for post in post_coll.find():
        all_post.append(post)

    return render_template('viewpost.html', all_post = all_post)
        