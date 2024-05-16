from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from app.repositories import user_repo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = user_repo.get(username=username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')