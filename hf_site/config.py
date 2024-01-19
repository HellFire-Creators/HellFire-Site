import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
    