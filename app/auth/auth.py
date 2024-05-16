from flask import Blueprint, render_template, current_app, redirect, url_for, session
from flask_login import login_user, logout_user, login_required

from app.utils import logged_out_required, ensure_url_param
from app.repositories import user_repo
from app.models import User
from app.remote import GithubRequestHandler
import app.auth.forms as forms


blueprint = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

@blueprint.route('/', methods=['GET'])
@logged_out_required
def authenticate():
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id={current_app.config["GITHUB_CLIENT_ID"]}'
    return render_template('authenticate.html', github_url = github_auth_url)

@blueprint.route('/github-callback', methods=['GET'])
@logged_out_required
@ensure_url_param(['code'], pass_param=True)
def github_callback(code):
    access_token = GithubRequestHandler.request(
        'POST',
        url='https://github.com/login/oauth/access_token',
        json={
            'client_id': current_app.config['GITHUB_CLIENT_ID'],
            'client_secret': current_app.config['GITHUB_SECRET'],
            'code': code
        },
        headers={
            "Accept": "application/json"
        }
    )['access_token']

    github_user = GithubRequestHandler.request(
        "GET", 
        url = 'https://api.github.com/user',
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {access_token}',
        }   
    )

    user = user_repo.get(github_id = github_user['id'])
    if user is None:
        user_repo.add(User(github_id = github_user['id'], is_active = False))
    elif user.is_active == True:
        login_user(user)
        return redirect(url_for('index.index'))
    
    session['github_id'] = github_user['id']
    return redirect(url_for('auth.register'))


@blueprint.route('/register', methods=['GET', 'POST'])
@logged_out_required
def register():
    github_id = session.get('github_id')
    user = user_repo.get(github_id=github_id, is_active=False)
    if user is None:
        return redirect(url_for('auth.authenticate'))

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        session.pop('github_id')
        user_repo.update(user.id, username=form.username.data, is_active=True)
        login_user(user)
        
        return redirect(url_for('index.index'))
    
    return render_template('register.html', title='Register', form=form)


@blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()

    return redirect(url_for('index.index'))