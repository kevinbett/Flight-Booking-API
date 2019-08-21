# api/tests/test_flights.py

import json
import unittest

from api.v1 import db
from api.v1.models import User, Flight
from api.tests.base import BaseTestCase


class FlightsTestCase(BaseTestCase):


    def test_create_flight(self):
        """ Flight creation test """
        response = self.create_flight(self.flight_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "Flight successfully added"
        )
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_duplicate_flight(self):
        flight = Flight(
            name="Trans mediteranean",
            origin="Dar",
            destination="NY",
            date="1/1/2020",
            departure_time="8/16/2019 06:00:00",
            arrival_time="1/1/2029 22:00:00"
        )
        db.session.add(flight)
        db.session.commit()

        response = self.create_flight(self.flight_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "Duplicate flight name"
        )
        self.assertTrue(data['status'] == 'failed')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 401)

    def test_create_incomplete_flight(self):
        """ Flight creation test """
        response = self.create_flight(self.incomplete_flight_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "PLease enter all the required flight details!"
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_flight_invalid_name(self):
        """ Flight creation test """
        response = self.create_flight(self.invalid_flight_name)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == "Flight name cannot have special characters!"
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)
