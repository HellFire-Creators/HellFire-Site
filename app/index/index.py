from flask import render_template, Blueprint
from flask_login import login_required


blueprint = Blueprint("index", __name__, template_folder="templates", static_folder="static")

@blueprint.route('/')
@login_required
def index():
    return render_template('index.html')