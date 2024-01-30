from flask import Blueprint

auth = Blueprint('auth', __name__)

from hellfire.auth import routes