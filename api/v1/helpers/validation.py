# api/v1/helpers/validation.py

import re


def validate_input(data):
    """
    User input validation
    """
    if len(data['email'].strip()) == 0:
        # Checks length of email
        return "Email cannot be blank."
    if len(data['password'].strip()) == 0:
        # Checks length of password
        return "Password cannot be blank."
    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", data['email']):
        # Checks email validity
        return "Please provide a valid email and try again"
    if not re.match("^[a-zA-Z0-9_]*$", data['username']):
        # Checks username validity
        return "Inalid username. Check and try again."
    if len(data['username'].strip()) < 3:
        # Checks length of username
        return "Username must have more than 3 characters."
    if len(data['password']) < 5 or not re.search("[a-z]", data['password']) or not\
            re.search("[0-9]", data['password']) or not re.search("[A-Z]", data['password']):
        # Checks password length
        return "Password must be more than 5 characters have one number and symbol"
    else:
        return data

def validate_flight(flight):
    if not flight['name'] or not flight['origin'] or \
    not flight['destination'] or not flight['date'] or not flight['departure_time'] \
    or not flight['arrival_time']:
        return "PLease enter all the required flight details!"

    elif not re.match("^[a-zA-Z0-9_ ]*$", flight['name'].strip()):
        return "Flight name cannot have special characters!"

    else:
        return flight

def validate_bookings(booking):
    if not booking['number_of_tickets'] or not booking['flight_id']:
        return "Please enter number of tickets and flight_id"

    else:
        return booking

def validate_get_bookings(booking):
    if not booking['flight_id']:
        return "Please enter the flight_id"

    else:
        return booking
