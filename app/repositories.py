from sqlalchemy.orm.exc import NoResultFound
from app.models import User, Project, ProjectPermission
from app.extensions import db

from abc import ABC, abstractmethod

class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    @property
    @abstractmethod
    def model(self):
        pass

    def get(self, **filters):
        try:
            return self.session.query(self.model).filter_by(**filters).one()
        except NoResultFound:
            return None

    def list(self, **filters):
        return self.session.query(self.model).filter_by(**filters).all()

    def add(self, object):
        self.session.add(object)
        self.session.commit()

    def update(self, object_id, **kwargs):
        project = self.get(id=object_id)
        if project:
            for key, value in kwargs.items():
                setattr(project, key, value)
            self.session.commit()
            return project
        return None

    def delete(self, object_id):
        object = self.get(id=object_id)
        if object:
            self.session.delete(object)
            self.session.commit()
            return True
        return False

class UserRepository(BaseRepository):
    @property
    def model(self):
        return User

class ProjectPermissionsRepository(BaseRepository):
    @property
    def model(self):
        return ProjectPermission

    def add(self, user, project, role):
        any(self.delete(role.id) for role in self.list(user_id = user.id, project_id = project.id))
        for role in role.inclusive_down:
            user_role = ProjectPermission(user_id = user.id, role_name = role, project_id = project.id)
            self.session.add(user_role)
        self.session.commit()

        # TODO reconsider how this is done

user_repo = UserRepository(db.session)
project_permissions_repo = ProjectPermissionsRepository(db.session)

from app.roles import ProjectPermissions

class ProjectRepository(BaseRepository):
    @property
    def model(self):
        return Project

    def add(self, object, owner):
        self.session.add(object)
        self.session.commit()
        try:
            project_permissions_repo.add(owner, object, ProjectPermissions.OWNER)
        except Exception as e:
            self.session.rollback()
            raise(e)

project_repo = ProjectRepository(db.session)