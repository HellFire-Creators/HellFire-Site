
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from app.roles import ProjectPermissions

# TODO Add more validation and such

class CreateProjectForm(FlaskForm):
    project_name = StringField('Name')
    description = StringField('Description')
    submit = SubmitField('CreateProject')


class ChangeUserRoleForm(FlaskForm):
    username = StringField('Username')
    roles_dropdown = SelectField('Roles', choices=[role.value for role in ProjectPermissions])
    submit = SubmitField('Add Role')
