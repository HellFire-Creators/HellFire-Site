from flask_sqlalchemy import SQLAlchemy
from flask_github import GitHub
from flask_jwt_extended import JWTManager

from flask import redirect, url_for

db = SQLAlchemy()
jwt = JWTManager()

from api.models.token_blocklist import TokenBlocklist

#Unused - I don't think this will be needed since its essentially a customizable 404, I'll leave it for now though
# TODO Plan out/think about auth on the backend
# @jwt.unauthorized_loader
# def custom_unauthorized_response(_err):
#     print(_err)
#     return redirect(url_for('auth.login'))

#Unused temporarily
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None