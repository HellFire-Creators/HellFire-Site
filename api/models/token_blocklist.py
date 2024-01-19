from sqlalchemy import Column, Integer, String, DateTime

from api.extensions import db

class TokenBlocklist(db.Model):
    __tablename__ = 'tokenBlocklist'
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)