from flask import request, url_for, redirect, make_response, render_template_string

from hf_site.main import bp
from hf_site.extensions import github

from functools import wraps
import requests
import json
import os

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.cookies.get('access_token')

        headers = {'Authorization': f'Bearer {access_token}'}
        url = 'http://127.0.0.1:3000/api/check-creds'
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.login'))
    return decorated_function

@bp.route('/')
@login_required
def index():
    return render_template_string("""You are logged in. <a href="{{ url_for('main.logout') }}"> Logout </a>""")

@bp.route('/login')
def login():
    redirect = github.authorize()
    url = redirect.location
    return render_template_string('<a href="{{url}}"> Login </a>', url=url)

@bp.route('/logout')
@login_required
def logout():
    # TODO Blocklist token in addition to removing it from cookies
    # TODO Research if I need to add one of those cookie popups? 99% sure I don't
    response = make_response(redirect(url_for('main.login')))
    response.set_cookie('access_token', '', expires=0)
    return response

@bp.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    #Immediatly return access token to use for getting user below
    @github.access_token_getter
    def token_getter():
        return access_token

    try:
        github_user = github.get('/user')
    except:
        # TODO Logging perhaps?
        # TODO Redirect to login page and include this message
        return f'Access token not found or invalid, please try again'
    
    # TODO Consider merging HellFire API and HellFire Site using blueprints so endpoints can be programatically obtained
    url = 'http://127.0.0.1:3000/api/get-user'

    data = {'id': github_user['id']}
    json_data = json.dumps(data)

    USER_JWT_SECRET = os.environ.get('USER_JWT_SECRET')
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {USER_JWT_SECRET}'}

    api_response = requests.get(url, data=json_data, headers=headers)

    if api_response.status_code == 200:
        api_response_data = api_response.json()
        access_token = api_response_data['access_token']

        response = make_response(redirect(url_for('main.index')))
        response.set_cookie('access_token', access_token)
        return response
    
    else:
        return redirect(url_for('main.login'))