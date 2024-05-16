from flask import Blueprint, render_template
from flask_login import login_required

from app.repositories import user_repo

blueprint = Blueprint("user", __name__, template_folder="templates", static_folder="static")


@blueprint.route('/<username>', methods=['GET'])
@login_required
def user(username):
    user = user_repo.get(username = username)

    return render_template('user.html', user=user)
