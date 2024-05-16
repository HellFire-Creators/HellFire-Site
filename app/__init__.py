from flask import Flask
from config import Config

from app.extensions import db, migrate, login_manager, sess

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app)
    sess.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.authenticate'


    with app.app_context():
        from app import roles

        db.create_all()
        roles.create_roles()

        from app.auth import auth
        from app.projects import projects
        from app.user import user
        from app.index import index

        app.register_blueprint(user.blueprint, url_prefix='/user')
        app.register_blueprint(projects.blueprint, url_prefix='/projects')
        app.register_blueprint(auth.blueprint, url_prefix='/auth')
        app.register_blueprint(index.blueprint)

        print(app.url_map)
        return app