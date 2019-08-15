from datetime import datetime, timedelta

from flask import render_template, jsonify, make_response
from flask_mail import Message, Mail
from api.v1.models import User, Flight, Booking

mail = Mail()


def handle_bookings():
    date = str((datetime.now() + timedelta(days=1)).date())
    bookings = Booking.query.filter(Booking.booking_date <= date).all()
    if not bookings:
        return False
    else:
        return bookings


def handle_message():
    bookings = handle_bookings()
    if not bookings:
        return False
    message_list = []
    for booking in bookings:
        user = User.query.filter_by(id=booking.user_id).first()
        flight = Flight.query.filter_by(id=booking.flight_id).first()
        msg = Message('Flight Reservation Reminder!',
            recipients=[user.email], sender="info@kenyaairways.com")
        msg.html = render_template('mail.html',
            name=user.name,
            flight_name=flight.name,
            departure_time=flight.departure_time
        )

        message_list.append(msg)

    return message_list


def handle_email():
    from manage import app
    with app.app_context():
        bookings = handle_bookings()
        if not bookings:
            print("We dont have a booking")
            return "No bookings"
        else:
            messages = handle_message()
            print("These are your messages")
            for message in messages:
                print("This is one message")
                try:
                    print("Trying")
                    with app.app_context():
                        print("Sending")
                        mail.send(message)

                except Exception as e:
                    return e
