import json
import unittest

from api.v1 import db
from api.v1.models import User, Flight, Booking
from api.tests.base import BaseTestCase


class BookingsTestCase(BaseTestCase):


    def test_book_flight(self):
        """ Flight creation test """
        flight = self.create_flight(self.flight_data)
        response = self.create_booking(self.booking_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "You have successfully booked your flight"
        )
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_book_non_existent_flight(self):
        """ book non existent flight test """
        response = self.create_booking(self.booking_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "Flight does not exist"
        )
        self.assertTrue(data['status'] == 'failed')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)


    def test_booking_with_blank_flight_id(self):
        """ book non existent flight test """
        response = self.create_booking(self.booking_blank_flight_id)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "Please enter number of tickets and flight_id"
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_booking_with_blank_fields(self):
        """ book non existent flight test """
        response = self.create_booking(self.booking_blank_fields)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "Please enter number of tickets and flight_id"
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_booking_with_empty_ticket(self):
        """ booking with empty ticket test """
        response = self.create_booking(self.booking_data_no_ticket)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "Please enter number of tickets and flight_id"
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_bookings(self):
        """ Get booking test """
        create_flight = self.create_flight(self.flight_data)
        book_flight = self.create_booking(self.booking_data)
        get_booking = self.get_booking(self.get_booking_data)
        response = json.loads(get_booking.data.decode())
        self.assertTrue(
            response == {'number_of_bookings': 1}
        )

    def test_get_bookings_for_non_existent_flight(self):
        """ Get booking test fo non existent flight """
        create_flight = self.create_flight(self.flight_data)
        book_flight = self.create_booking(self.booking_data)
        get_booking = self.get_booking(self.get_booking_data_no_flight)
        response = json.loads(get_booking.data.decode())
        self.assertTrue(
            response['message'] == "No bookings available"
        )
        self.assertTrue(response['status'] == 'failed')

    def test_get_bookings_no_id(self):
        """ Get booking test fo no id """
        create_flight = self.create_flight(self.flight_data)
        book_flight = self.create_booking(self.booking_data)
        get_booking = self.get_booking(self.get_booking_data_no_id)
        response = json.loads(get_booking.data.decode())
        self.assertTrue(
            response['message'] == "Please enter the flight_id"
        )
