from flask import Response, Flask, jsonify, make_response, url_for, render_template, \
    send_from_directory, request, url_for, redirect, flash, Blueprint
from flask_login import LoginManager, login_required, login_user, current_user,logout_user
from flask_bootstrap import Bootstrap
from pymongo import MongoClient, DESCENDING, IndexModel, TEXT
from datetime import datetime, timedelta
from blueprints.site.forms import NewPostForm, NewCommentForm
from bson.objectid import ObjectId
from blueprints.login.routes import mod
from blueprints.site.User import User
from pymongo import MongoClient
from blueprints.db_config import *
from flask import jsonify

mod = Blueprint('site',__name__, template_folder= 'templates')


'''
db initialization and login_manager init
LoginManager() has be be initialized in any blueprint
that uses the User class
'''
login_manager = LoginManager()
client = MongoClient(server_url)
db = client[db_server_name]
db.authenticate(db_user, db_pass)
user_coll = db[user_collection]
post_coll = db[post_collection]
comments_coll = db[comments_collection]

'''
not sure if I need this or not,
but loads login_manager for blueprint
'''
@mod.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(username):  
    u = user_coll.find_one({"username": username})
    if not u:
        return None

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

        return redirect(url_for('site.viewuserposts'))
    return render_template('site/newpost.html', form=form)


@mod.route("/viewuserposts")
@login_required
def viewuserposts():
    '''
    view all current users post
    '''

    all_post = []
    for post in post_coll.find({'username':current_user.get_id()}):

        post_id = str(ObjectId(post['_id']))
        post['post_url'] = url_for('site.viewpost', id=post_id)
        all_post.append(post)
    return render_template('site/viewuserposts.html', all_post=all_post)


@mod.route("/viewallposts")
@login_required
def viewallposts():
    '''
    view all posts
    '''

    all_post = []
    for post in post_coll.find():

        post_id = str(ObjectId(post['_id']))
        post['post_url'] = url_for('site.viewpost', id=post_id)
        all_post.append(post)
    return render_template('site/viewallposts.html', all_post=all_post)



@mod.route("/viewpost/<id>", methods=['GET', 'POST'])
@login_required
def viewpost(id):
    post = {}
    form = NewCommentForm(request.form)
    comments = []

    '''
    check and validate comment form
    '''
    if request.method == 'POST' and form.validate():
        username = current_user.get_id()
        comment = form.comment.data
        created_datetime = datetime.utcnow()
        edited_datetime = datetime.utcnow()

        '''
        once from is valid, check if its in the right post
        after that insert the comment into the comments-collection
        '''
        if post_coll.find_one({'_id':ObjectId(id)}):
            comments_coll.insert({'post_id': ObjectId(id),
                                    'username': current_user.get_id(),
                                    'comment': comment,
                                    'created_datetime': created_datetime,
                                    'edited_datetime': edited_datetime})
            return redirect(url_for('site.viewpost', id=id))

    '''
    retreives all comments and appends them to comments array
    '''
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

@mod.route("/viewallpostsapi")
def viewallpostsapi():
    '''
    view all posts
    '''

    all_post = []
    for post in post_coll.find():
        print(post)
        post['_id'] = str(ObjectId(post['_id']))
        post_id = str(ObjectId(post['_id']))
        post['post_url'] = url_for('site.viewpost', id=post_id)
        all_post.append(post)
        print(post)
    return jsonify(all_post)
