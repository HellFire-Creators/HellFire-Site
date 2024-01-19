
from flask import Flask

from api.config import Config

app = Flask(__name__)
app.config.from_object(Config)

#Extensions
from api.extensions import db, jwt
db.init_app(app)
jwt.init_app(app)

#Blueprints
from api.users import bp as auth
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()