
from sqlalchemy import Column, Integer, String, Table, ForeignKey, and_

from hellfire.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class ProjectPermissions(db.Model):
    __tablename__ = 'project_permissions'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)