from flask_bcrypt import Bcrypt
#https://flask-bcrypt.readthedocs.io/en/latest/
#https://runningcodes.net/flask-login-and-mongodb/
#https://github.com/boh717/FlaskLogin-and-pymongo

class User():

    def __init__(self, username):
        self.username = username
        self.email = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)