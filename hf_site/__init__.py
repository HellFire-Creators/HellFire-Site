
from flask import Flask

from hf_site.config import Config

#CREATE APP
app = Flask(__name__)
app.config.from_object(Config)

#Extensions
from hf_site.extensions import github
github.init_app(app)

#Blueprints
from hf_site.main import bp as main
app.register_blueprint(main)

if __name__ == "__main__":
    app.run()