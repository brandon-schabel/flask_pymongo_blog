from flask import Response, Flask, jsonify, make_response, url_for, render_template, \
    send_from_directory, request, url_for, redirect, flash, Blueprint
from flask_login import LoginManager, login_required, login_user, current_user,logout_user
from datetime import datetime, timedelta
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from blueprints.login.login_config import *
from bson.objectid import ObjectId
from blueprints.login.forms import LoginForm, RegistrationForm
from pymongo import MongoClient
from blueprints import app
from blueprints.login.User import User

client = MongoClient(server_url)
db = client[db_server_name]
db.authenticate(db_user, db_pass)
user_coll = db[user_collection]

mod = Blueprint('login',__name__, template_folder= 'templates')

login_manager = LoginManager()

#login_manager.init_app(mod)
#login_manager.loging_view = 'login'

@mod.record_once
def on_load(state):
    login_manager.init_app(state.app)
    bcrypt = Bcrypt(state.app)

@login_manager.user_loader
def load_user(username):  
    u = user_coll.find_one({"username": username})
    if not u:
        return None
    
    return User(u['username'])

@mod.route('/login', methods=['GET', 'POST'])
def login():
    bcrypt = Bcrypt(app)
    error = None
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():

        #form data loader
        form_email = form.login_email.data
        form_password = form.password.data

        #DB user loader
        if(user_coll.find_one({'email':form_email})):   
            user = user_coll.find_one({'email':form_email})
            user_email = user['email']
            user_pass = user['password']
            username = user['username']
            #if form email is equal to the email from the database
            if(form_email == user_email):
                #if password from database is the same as the form password
                if(bcrypt.check_password_hash(user_pass, form_password)):
                    user_obj = User(user['username'])
                    login_user(user_obj)
                    flash('You were successfully logged in')
                    return redirect(url_for('site.viewpost'))

                else:
                    error = "Invalid email or password."
            print(user_email)
        else:
            error = "Invalid email or password"

    return render_template('login/login.html', form=form, error = error)

    
@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    error = None
    
    if request.method == 'POST' and form.validate():
        username = form.login_username.data
        email = form.login_email.data
        password_hashed = bcrypt.generate_password_hash(form.password.data)

        if (user_coll.find_one({'email':email})) == None:
            if (user_coll.find_one({'username': username})) == None:
                data_to_log = {
                    'username': username,
                    'email': email,
                    'password': password_hashed
                }
                user_coll.insert(data_to_log)
                flash('You were successfully registered!')
                return redirect(url_for('index'))
            else:
                error = "Username taken"
        else:
            error = "Email already in use"
        
    return render_template('login/register.html', form=form,error = error)

@mod.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.index'))