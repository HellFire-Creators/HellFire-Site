from hellfire.auth import auth
from hellfire.extensions import github, db
from hellfire.models.user import User

from flask import redirect, url_for, render_template_string
from flask_login import current_user, login_user, login_required, logout_user



@auth.route('/', methods=['GET'])
def authenticate():
    if current_user.is_authenticated:
        # TODO make this redirect to next param (make sure to validate next param)
        return redirect(url_for("site.index"))
    redirect_url = github.authorize().location
    return render_template_string('<a href="{{url}}"> Authorize with Github </a>', url=redirect_url)

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.authenticate"))
    
@auth.route('/github-callback', methods=['GET'])
@github.authorized_handler
def github_callback(access_token):
    #region Get User
    @github.access_token_getter
    def token_getter():
        return access_token
    try:
        github_user = github.get('/user')
    except:
        # TODO Logging perhaps?
        # TODO Redirect to login page and include this message
        return f'Access token not found or invalid, please try again'
    #endregion
    
    github_id = github_user['id']
    try:
        user = User.query.filter_by(github_id=github_id).first()
        login_user(user)
        
        # TODO make this redirect to next param (make sure to validate next param)
        return redirect(url_for("site.index"))
    except:
        user = User(github_id)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("auth.new_user_callback"))
    
@auth.route('/new-user-callback', methods=['GET'])
@login_required
def new_user_callback():
    # TODO Ask for addtional user info here, and
    # TODO make this redirect to next param (make sure to validate next param)
    return render_template_string('<a href="{{ url_for("site.index") }}"> Go to home </a>')