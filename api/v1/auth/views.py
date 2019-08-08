# api/v1/auth/views.py

from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask.views import MethodView

from api.v1 import bcrypt, db
from api.v1.models import User, BlacklistToken

auth_blueprint = Blueprint('auth', __name__)


class Register(MethodView):
    """
    User Registration
    """

    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            try:
                user = User(
                    name=data.get('name'),
                    email=data.get('email'),
                    password=data.get('password')
                )

                # Add user to database
                user.save()

                # Generate auth token
                # auth_token = user.encode_auth_token(user.id)
                access_token = create_access_token(identity=user.id)
                response = {
                    'status': 'success',
                    'message': 'You have been successfully registered.',
                    'auth_token': access_token
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'status': 'failed',
                    'message': 'Error. Please try again.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'failed',
                'message': 'User is already registered. Please log in'
            }
            return make_response(jsonify(response)), 202


class Login(MethodView):
    """
    User Login
    """

    def post(self):
        data = request.get_json()
        try:
            user = User.query.filter_by(
                email=data.get('email')
            ).first()
            if not user:
                response = {
                    'status': 'failed',
                    'message': 'User does not exist, please sign up'
                }
                return make_response(jsonify(response)), 404

            if user and bcrypt.check_password_hash(
                user.password, data.get('password')
            ):
                # auth_token = user.encode_auth_token(user.id)
                access_token = create_access_token(identity=user.id)
                if access_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in',
                        'auth_token': access_token
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'status': 'failed',
                    'message': 'Please check your password and try again'
                }
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {
                'status': 'failed',
                'message': 'Please Try again'
            }
            print(e)
            return make_response(jsonify(response)), 500


class GetUser(MethodView):
    """
    List users
    """

    def get(self):
        # Get token
        header = request.headers.get('Authorization')
        if header:
            try:
                auth_token = header.split(" ")[1]
            except IndexError:
                response = {
                    'status': 'fail',
                    'message': 'Invalid bearer token.'
                }
                return make_response(jsonify(response))
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.dmin,
                        'registered_on': user.reg_date
                    }
                }
                return make_response(jsonify(response)), 200
            response = {
                'status': 'failed',
                'message': resp
            }
            return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'failed',
                'Message': 'Invalid Token'
            }
            return make_response(jsonify(response))


class Logout(MethodView):
    """
    Log out
    """

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
            return make_response("You are not logged in"), 403
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # Blacklist token
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response = {
                        'status': 'success',
                        'Message': 'you have been successfully logged out'
                    }
                    return make_response(jsonify(response)), 200
                except Exception as e:
                    response = {
                        'status': 'failed',
                        'message': 'e'
                    }
                    return make_response(jsonify(response)), 401
            else:
                response = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return make_response(jsonify(response)), 403


# Api endpoints
registration_view = Register.as_view('register')
login_view = Login.as_view('login')
user_view = GetUser.as_view('users')
logout_view = Logout.as_view('logout')


# Rules
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/users',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
