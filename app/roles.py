from enum import Enum
from app.extensions import db

#this thing kind of feels scuffed
class ProjectPermissions(Enum):
    OWNER = 'Owner'
    MANAGER = 'Manager'
    MEMBER = 'Member'
    VIEWER = 'Viewer'

    @property
    def inclusive_down(self):
        roles = [role.value for role in list(ProjectPermissions)]
        index = roles.index(self.value)
        return roles[index:]
    
    @property
    def inclusive_up(self):
        roles = [role.value for role in list(ProjectPermissions)]
        index = roles.index(self.value)
        return roles[:index + 1]

from app.models import Permission

def create_roles():
    for role_enum in ProjectPermissions:
        role = Permission.query.filter_by(name=role_enum.value).first()
        if not role:
            role = Permission(name=role_enum.value)
            db.session.add(role)
    db.session.commit()