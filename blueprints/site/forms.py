from wtforms import Form, BooleanField, StringField, IntegerField, PasswordField, TextAreaField, validators

class NewPostForm(Form):
    post_title = StringField (u'Post Title', validators=[validators.input_required()])
    post_content = TextAreaField(u'Post Name', validators=[validators.optional(), validators.length(max=20000)])
