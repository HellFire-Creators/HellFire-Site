from hellfire.site.models.project import Permission, ProjectPermissions, Project
from hellfire.extensions import db
from sqlalchemy import and_

def get_or_create_permission(name):
    permission = Permission.query.filter_by(name=name).first()
    if not permission:
        permission = Permission(name=name)
        db.session.add(permission)
        db.session.commit()
    return permission

def add_user_permission(user_id, project_id, permission_name):
    perm = get_or_create_permission(permission_name)
    project_permission = ProjectPermissions(user_id=user_id, project_id=project_id, permission_id=perm.id)
    db.session.add(project_permission)
    db.session.commit()

def check_user_permission_for_project(user_id, project_id, permission_name):
    pass

def get_projects_for_user_with_permission(user_id, permission):
    permission_id = get_or_create_permission(permission).id

    project_ids = ProjectPermissions.query.filter(and_(
        ProjectPermissions.user_id == user_id,
        ProjectPermissions.permission_id == permission_id
    )).with_entities(ProjectPermissions.project_id).all()

    result = []
    for id in project_ids:
        project = Project.query.filter_by(id=id[0]).first()
        if project:
            result.append({'id': project.id, 'name': project.name, 'description': project.description})

    return result

def modify_project(project_id, project_name, description):
    project = Project.query.filter_by(id=project_id).first()
    project.name = project_name
    project.description = description
    db.session.add(project)
    db.session.commit()

def create_project(user_id, project_name, description=None):
    project = Project(project_name, description=description)
    db.session.add(project)
    db.session.commit()
    add_user_permission(user_id, project.id, 'read')

def delete_projects(user_id, projects):
    import pprint
    user_projects = get_projects_for_user_with_permission(user_id, 'read')

    user_project_ids = [project['id'] for project in user_projects]

    to_be_deleted = [project['id'] for project in projects if project['id'] in user_project_ids]

    pprint.pprint(f"USER PROJECTS: {user_projects}")
    pprint.pprint(f"TO BE DELETED: {to_be_deleted}")
    for id in to_be_deleted:
        Project.query.filter_by(id=id).delete()
        ProjectPermissions.query.filter_by(project_id=id).delete()
    db.session.commit()