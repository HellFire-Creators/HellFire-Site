
from sqlalchemy import Column, Integer, String, DateTime

from api.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    github_id = Column(Integer)
    github_login = Column(String(255))
    github_email = Column(String(255))

    minecraft_username = Column(String(255))

    discord_username = Column(String(255))

    def __init__(self, github_id):
        self.github_id = github_id