from flask import g
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from Mood.models import User


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=6)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_pic = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    # check for duplicate username + user's username != keyed in username
    def validate_username(self, username):
        if username.data != g.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self, email):
        if email.data != g.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose a different one')