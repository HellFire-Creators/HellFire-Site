from flask import jsonify
from flask import request, g, redirect, url_for


from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from flask_expects_json import expects_json

from api.users import bp
from api.extensions import jwt, db
from api.models.user import User
from api.models.token_blocklist import TokenBlocklist

from datetime import datetime, timedelta, timezone
import json
import os
from functools import wraps

# TODO MAKE SURE THIS IS SAFE - USE STATE PARAM
# TODO Validate JSON
@bp.route('/get-user')
def get_user():
    data = json.loads(request.data)

    #Ensure that this view is restricted to frontend
    # TODO Research is there a better way to do this?
    USER_JWT_SECRET = os.environ.get('USER_JWT_SECRET')


    authorization_header = request.headers['Authorization']
    PREFIX = 'Bearer '
    authorization_token = authorization_header[len(PREFIX):]

    if USER_JWT_SECRET != authorization_token:
        return jsonify({
            'msg': 'Forbidden'
        }), 404
    
    github_id = data['id']

    try:
        user = User.query.filter_by(github_id=github_id).first()
        access_token = create_access_token(identity=user.github_id)
        return jsonify({
            'access_token': access_token,
            'msg': 'User found'
        }), 200
    
    except Exception as e:
        user = User(github_id)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.github_id)

        # TODO Possibly invalidate previous user JWT's? This could cause the issue of logging the user out on other devices, but in theory is fine.
        # TODO Additionally, implement token timeout, as well as refresh tokens
        # TODO Consider if its neccesary to store the Github token for some purpose possibly.
        return jsonify({
            'access_token': access_token,
            'msg': 'New user created',
        }), 200

@bp.route('/check-creds', methods=['GET'])
@jwt_required()
def check_creds():
    return jsonify({
            'msg': 'Credentials are valid'
        }), 200

#TODO Add functionality to generate API Tokens - PLAN THIS OUT BEFOREHAND