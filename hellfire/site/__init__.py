from flask import Blueprint

site = Blueprint('site', __name__)

from hellfire.site import routes