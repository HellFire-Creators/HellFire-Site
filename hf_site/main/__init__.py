from flask import Blueprint

bp = Blueprint('main', __name__)

from hf_site.main import routes