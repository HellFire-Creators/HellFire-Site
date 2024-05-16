from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.Integer, index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    _is_active = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    @hybrid_property
    def is_active(self):
        return self._is_active
    
    @is_active.setter
    def is_active(self, value: bool):
        self._is_active = value


class Permission(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class ProjectPermission(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_name = db.Column(db.Integer(), db.ForeignKey('roles.name', ondelete='CASCADE'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<User Role, Self ID: {self.id}, User ID: {self.user_id}, Role Name: {self.role_name}, Project : {self.project_id}>'


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Project {}>'.format(self.name)
    
from app.repositories import user_repo
@login_manager.user_loader
def load_user(id):
    return user_repo.get(id=id)