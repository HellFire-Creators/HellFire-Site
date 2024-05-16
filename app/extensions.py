from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_session import Session

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate(db=db)
sess = Session()