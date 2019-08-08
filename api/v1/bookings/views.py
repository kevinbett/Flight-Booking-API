from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime

from api.v1.models import User, Booking, Flight

booking_blueprint = Blueprint('booking', __name__)


class FlightBooking(MethodView):
    """
    End point to book a flight
    """
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        ticket_quantity = data['number_of_tickets']
        flight_id = data['flight_id']

        check_flight = Flight.query.filter_by(id=flight_id).first()
        if not check_flight:
            response = {
                'status': 'failed',
                'message': 'Flight does not exist'
            }
            return make_response(jsonify(response)), 400
        date = datetime.date.today()
        booking = Booking(
            user_id = user_id,
            tickets = ticket_quantity,
            flight_id = flight_id,
            booking_date = date
        )

        booking.save()

        response = {
            'status' : 'success',
            'message' : 'You have successfully booked your flight'
        }
        return make_response(jsonify(response)), 201

# APi endpoint
booking_view = FlightBooking.as_view('flightbooking')

#Rules
booking_blueprint.add_url_rule('/booking/flightbooking', view_func=booking_view)
