from flask import Blueprint

bp = Blueprint('auth', __name__)

# TODO users directory should probably be changed to auth

from api.users import routes