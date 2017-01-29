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

