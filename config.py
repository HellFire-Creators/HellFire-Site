import os
from cryptography.fernet import Fernet
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    GITHUB_SECRET = os.environ.get('GITHUB_SECRET')
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    ENCRYPTION_KEY = Fernet.generate_key()
    RBAC_USE_WHITE = True
    SESSION_TYPE = 'filesystem'