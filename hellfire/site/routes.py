from hellfire.site import site

from flask import render_template_string, request, render_template, redirect, url_for
from htmx_flask import make_response
from flask_login import current_user, login_required

from hellfire.site.db.projects_data import create_project, get_projects, delete_projects, modify_project

@site.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        project_name = request.form.get('name')
        project_description = request.form.get('description')
        create_project(current_user.id, project_name, description=project_description)
        print(project_name)

    projects = get_projects(current_user.id, 'read')

    return render_template("index.html", user_projects=projects)

@site.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def project(id: int):
    projects = get_projects(current_user.id, 'read')
    project_ids = [project['id'] for project in projects]
    if id not in project_ids:
        return {}, 404

    if request.method == 'PUT':
        project_name = request.form.get('name')
        project_description = request.form.get('description')
        modify_project(current_user.id, id, project_name, project_description)
    

    projects = get_projects(current_user.id, 'read')
    for project in projects:
        if project['id'] == id:
            current_project = project
            break
    
    if request.method == 'DELETE':
        delete_projects(current_user.id, [current_project])

        return make_response(
        'test',
        redirect=url_for("site.index"),
        )

    return render_template("project.html", id=id, project_name=current_project['name'], project_description=current_project['description'])