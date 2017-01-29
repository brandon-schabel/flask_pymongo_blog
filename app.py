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
from forms import LoginForm, RegistrationForm
from bson.objectid import ObjectId

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.loging_view = 'login'
Bootstrap(app)
bcrypt = Bcrypt(app)

app.config.update(SECRET_KEY= update_sec_key())

@login_manager.user_loader
def load_user(username):  
    u = user_coll.find_one({"username": username})
    if not u:
        return None
    
    return User(u['username'])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
                    return redirect(url_for('view'))

                else:
                    error = "Invalid email or password."
            print(user_email)
        else:
            error = "Invalid email or password"

    return render_template('login.html', form=form, error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_coll = db['user-database']
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
        
    return render_template('register.html', form=form,error = error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    #app.run(debug=True)
    # get port assigned by OS else set it to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=True)