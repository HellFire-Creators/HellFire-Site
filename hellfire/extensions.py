from flask_sqlalchemy import SQLAlchemy
from flask_github import GitHub
from flask_login import LoginManager


db = SQLAlchemy()

github = GitHub()

login_manager = LoginManager()
login_manager.login_view = "auth.authenticate"
login_manager.add_context_processor = True


from hellfire.site.models.user import User
   
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)