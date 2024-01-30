
from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#Extensions
from hellfire.extensions import db, github, login_manager
db.init_app(app)
github.init_app(app)
login_manager.init_app(app)

#Blueprints
from hellfire.api import api
from hellfire.site import site
from hellfire.auth import auth
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(site)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()