
from functools import wraps
from flask import redirect, url_for, request, abort
from flask_login import current_user

def logged_out_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('index.index'))
        return f(*args, **kwargs)
    return decorated_function


def ensure_url_param(params: list, pass_param=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for param_name in params:
                param_value = request.args.get(param_name)
                if param_value is None:
                    abort(400, f"Missing '{param_name}' parameter in the URL")
                if pass_param:
                    kwargs[param_name] = param_value
            return f(*args, **kwargs)
        return decorated_function
    return decorator
