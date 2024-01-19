from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound

from api import app as hf_api
from hf_site import app as hf_site

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound(), {
    '': hf_site,
    "/api": hf_api,
})

if __name__ == "__main__":
    app.run()