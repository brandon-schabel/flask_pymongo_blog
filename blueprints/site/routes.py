from flask import Response, Flask, jsonify, make_response, url_for, render_template, \
    send_from_directory, request, url_for, redirect, flash, Blueprint
from flask_login import LoginManager, login_required, login_user, current_user,logout_user
from flask_bootstrap import Bootstrap
from pymongo import MongoClient, DESCENDING, IndexModel, TEXT
from datetime import datetime, timedelta
#from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from blueprints.site.forms import NewPostForm, NewCommentForm
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
comments_coll = db[comments_collection]
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
            {'username': username,
             'post_title': post_title, 
             'post_content': post_content,
             'created_datetime':datetime.utcnow(),
             'edited_datetime': datetime.utcnow(),
             'post_comments': [],
             'is_favorite' : False})

        return redirect(url_for('site.index'))
    return render_template('site/newpost.html', form=form)


@mod.route("/viewallpost")
@login_required
def viewallpost():
    all_post = []
    for post in post_coll.find({'username':current_user.get_id()}):

        post_id = str(ObjectId(post['_id']))
        post['post_url'] = url_for('site.viewpost', id=post_id)
        #print (post['post_url'])
        all_post.append(post)
    return render_template('site/viewallpost.html', all_post=all_post)



@mod.route("/viewpost/<id>", methods=['GET', 'POST'])
@login_required
def viewpost(id):
    form = NewCommentForm(request.form)
    comments =[]
    if request.method == 'POST' and form.validate():
        username = current_user.get_id()
        comment = form.comment.data
        created_datetime = datetime.utcnow()
        edited_datetime = datetime.utcnow()

        if post_coll.find_one({'_id':ObjectId(id)}):
            comments_coll.insert({'post_id': ObjectId(id),
                                    'username': current_user.get_id(),
                                    'comment': comment,
                                    'created_datetime': created_datetime,
                                    'edited_datetime': edited_datetime})
            return redirect(url_for('site.viewpost', id=id))

    if post_coll.find_one({'_id':ObjectId(id)}):
        post = post_coll.find_one({'_id':ObjectId(id)})
        comments = []
        if(comments_coll.find_one({'post_id':ObjectId(id)})):
            for comment in comments_coll.find({'post_id':ObjectId(id)}):
                comments.append(comment)
    else:
        print("Post does not exit")
        return redirect(url_for('site.index'))
    return render_template('site/viewpost.html', comments=comments, post=post, form=form)



'''
def post_comment(post_id):
    form = NewCommentForm(request.form)
    if request.method == 'POST' and form.validate():
        if post_coll.find_one({'_id':ObjectId(post_id)}):

def view_comments(post_id):
    for comment in 
'''