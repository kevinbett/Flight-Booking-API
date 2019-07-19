# api/v1/flight/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from api.v1 import bcrypt, db
from api.v1.models import User, Flight, BlacklistToken
from api.v1.helpers.check_admin import check_admin

flight_blueprint = Blueprint('flight', __name__)


class CreateFlight(MethodView):
    """
    Flight creation
    """
    @jwt_required
    def post(self):
        user = get_jwt_identity()
        try:
            check_admin(user)
        except AssertionError as error:
            return make_response(jsonify({'error': error.args[0]}), 403)
        data = request.get_json()
        flight = Flight.query.filter_by(name=data.get('name')).first()
        if not flight:
            try:
                flight = Flight(
                    name=data.get('name'),
                    origin=data.get('origin'),
                    destination=data.get('destination'),
                    date=data.get('date'),
                    departure_time=data.get('departure_time'),
                    arrival_time=data.get('arrival_time')
                )

                flight.save()

                response = {
                    'status': 'success',
                    'message': 'Flight successfully added'
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'status': 'failed',
                    'message': e
                }
                return make_response(jsonify(response)), 401

        else:
            response = {
                'status': 'failed',
                'message': 'Duplicate flight name'
            }
            return make_response(jsonify(response)), 401


# Api endpoints
flight_view = CreateFlight.as_view('createflight')

# Rules
flight_blueprint.add_url_rule(
    '/flight/createflight',
    view_func=flight_view,
    methods=['POST']
)
