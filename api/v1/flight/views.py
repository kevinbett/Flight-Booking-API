# api/v1/flight/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.v1.models import User, Flight, Booking
from api.v1.helpers.check_admin import check_admin
from api.v1.helpers.validation import validate_flight

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

        name = data['name'].strip()
        origin = data['origin']
        destination = data['destination']
        departure_time = data['departure_time']
        arrival_time = data['arrival_time']
        flight_details = validate_flight(data)

        if flight_details is not data:
            return jsonify({"message":flight_details}), 400

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


class GetBookings(MethodView):
    """
    End point to get bookings per flight
    """
    @jwt_required
    def get(self):
        data = request.get_json()

        bookings = Booking.query.filter_by(
            flight_id=data.get('flight_id')).all()
        if not bookings:
            response = {
                "status": "failed",
                "message": "No bookings available"
            }
            return make_response(jsonify(response)), 401
        booking_number = []
        for booking in bookings:
            booking_number.append(booking)
        response = {
            'number_of_bookings': len(booking_number)
        }
        return make_response(jsonify(response)), 200


# Api endpoints
flight_view = CreateFlight.as_view('createflight')
bookings_view = GetBookings.as_view('getbookings')

# Rules
flight_blueprint.add_url_rule(
    '/flight/createflight',
    view_func=flight_view,
    methods=['POST']
)
flight_blueprint.add_url_rule(
    '/flight/getbookings', view_func=bookings_view, methods=['GET'])
