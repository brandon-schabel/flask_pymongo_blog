from wtforms import Form, BooleanField, StringField, IntegerField, PasswordField, validators

class LoginForm(Form):
    login_email = StringField(u'Email',validators=[validators.input_required()])
    password = PasswordField(u'Password', validators=[validators.input_required()])

class RegistrationForm(Form):
    login_username = StringField (u'Username', validators=[validators.input_required()])
    login_email = StringField (u'Email', validators=[validators.input_required()])#validators.Email(), validators.EqualTo('confirm_email', message='Emails must match')
    confirm_email = StringField(u'Repeat Email', [validators.input_required()])
    password = PasswordField(u'Password', validators=[validators.input_required()])#, validators.EqualTo('confirm_pass', message='Passwords must match')
    confirm_pass = PasswordField(u'Repeat Password',validators=[validators.input_required()])