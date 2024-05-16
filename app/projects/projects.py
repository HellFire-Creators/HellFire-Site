from flask import Blueprint, render_template,redirect, url_for
from flask_login import login_required, current_user

from app.repositories import user_repo, project_repo, project_permissions_repo
from app.roles import ProjectPermissions
from app.models import Project
import app.projects.forms as forms


blueprint = Blueprint("projects", __name__, template_folder="templates", static_folder="static")


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def projects():
    form = forms.CreateProjectForm()
    if form.validate_on_submit():
        new_project = Project(name=form.project_name.data, description=form.description.data)
        project_repo.add(new_project, current_user)

        return redirect(url_for('projects.project', project_name = form.project_name.data))
    
    user_permissions_for_project = project_permissions_repo.list(user_id = current_user.id, role_name=ProjectPermissions.VIEWER.value)
    projects = [project_repo.get(id=role.project_id) for role in user_permissions_for_project]

    return render_template('projects.html', form=form, projects=projects)


@blueprint.route('/<project_name>')
@login_required
def project(project_name):
    current_project = project_repo.get(name=project_name)
    role = project_permissions_repo.get(user_id=current_user.id, project_id=current_project.id, role_name=ProjectPermissions.VIEWER.value)

    if role is None:
        return redirect(url_for('index.index'))
    
    return render_template('project.html', project_name=current_project.name)


@blueprint.route('/<project_name>/roles', methods=['GET', 'POST'])
@login_required
def project_roles(project_name):
    current_project = project_repo.get(name=project_name)
    role = project_permissions_repo.get(user_id=current_user.id, project_id=current_project.id, role_name=ProjectPermissions.VIEWER.value)

    if role is None:
        return redirect(url_for('index.index'))
    
    form = forms.ChangeUserRoleForm()
    if form.validate_on_submit():
        if project_permissions_repo.get(user_id=current_user.id, project_id=current_project.id, role_name=ProjectPermissions.MANAGER.value):
            user = user_repo.get(username = form.username.data)
            project_permissions_repo.add(user, current_project, ProjectPermissions(form.roles_dropdown.data))


    role_user_dict = {role.value: [] for role in ProjectPermissions}
    for role in ProjectPermissions:
        user_roles = project_permissions_repo.list(project_id=current_project.id, role_name=role.value)
        users_with_role = [user_repo.get(id=user_role.user_id).username for user_role in user_roles]

        users_to_include = [
            user for user in users_with_role
            if user not in [item for sublist in role_user_dict.values() for item in sublist]
        ]

        role_user_dict[role.value].extend(users_to_include)

    role_options = [role.value for role in ProjectPermissions]
    return render_template('project_roles.html', form=form, project_name=project_name, project_roles=role_user_dict, role_options=role_options)