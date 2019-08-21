from flask_testing import TestCase

from api.v1 import app, db

import json


class BaseTestCase(TestCase):
    """Base Test"""

    def create_app(self):
        app.config.from_object('api.v1.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

        self.registration_data = {
            'username': 'Kevin',
            'email': 'bettkevin757@gmail.com',
            'password': 'Password@1',
            'admin': 'True'
        }

        self.login_data = {
            'email': 'bettkevin757@gmail.com',
            'password': 'Password@1',
        }

        self.none_registered_login_data = {
            'email': 'noneregistered@gmail.com',
            'password': 'Password@1',
        }

        self.invalid_username_data = {
            'username': 'Kevin#',
            'email': 'invalid@gmail.com',
            'password': 'Password@1',
        }

        self.invalid_email_data = {
            'username': 'Kevin#',
            'email': 'invalidgmail.com',
            'password': 'Password@1',
        }

        self.short_username_data = {
            'username': 'Ke',
            'email': 'shortusername@gmail.com',
            'password': 'Password@1',
        }

        self.invalid_password_data = {
            'username': 'Kevin',
            'email': 'invalidpass@gmail.com',
            'password': 'pass',
        }

        self.wrong_password_data = {
            'username': 'Kevin',
            'email': 'bettkevin757@gmail.com',
            'password': 'Password@2',
        }

        self.flight_data = {
            "name": "Trans mediteranean",
            "origin": "Dar",
            "destination": "NY",
            "date": "1/1/2020",
            "departure_time": "8/16/2019 06:00:00",
            "arrival_time": "1/1/2029 22:00:00"
        }

        self.incomplete_flight_data = {
            "name": "",
            "origin": "Dar",
            "destination": "NY",
            "date": "1/1/2020",
            "departure_time": "8/16/2019 06:00:00",
            "arrival_time": "1/1/2029 22:00:00"
        }

        self.invalid_flight_name = {
            "name": "Chicago#",
            "origin": "Dar",
            "destination": "NY",
            "date": "1/1/2020",
            "departure_time": "8/16/2019 06:00:00",
            "arrival_time": "1/1/2029 22:00:00"
        }

        self.booking_data = {
            "number_of_tickets": "3",
            "flight_id": "1"
        }

        self.booking_data_no_ticket = {
            "number_of_tickets": "",
            "flight_id": "1"
        }

        self.booking_blank_flight_id = {
            "number_of_tickets": "3",
            "flight_id": ""
        }

        self.booking_blank_fields = {
            "number_of_tickets": "",
            "flight_id": ""
        }

        self.get_booking_data = {
            "flight_id": "1"
        }

        self.get_booking_data_no_flight = {
            "flight_id": "10"
        }

        self.get_booking_data_no_id = {
            "flight_id": ""
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self, data):
        return self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

    def login_user(self, data):
        return self.client.post(
            'auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )

    def get_token(self):
        self.register_user(self.registration_data)
        res = self.login_user(self.login_data)
        data = json.loads(res.data.decode())
        access_token = data['auth_token']
        return "Bearer " + access_token

    def create_flight(self, data):
        return self.client.post(
            'flight/createflight',
            data=json.dumps(data),
            content_type='application/json',
            headers=dict(Authorization=self.get_token())
        )

    def create_booking(self, data):
        return self.client.post(
            'booking/flightbooking',
            data=json.dumps(data),
            content_type='application/json',
            headers=dict(Authorization=self.get_token())
        )

    def get_booking(self, data):
        return self.client.get(
            'flight/getbookings',
            data=json.dumps(data),
            content_type='application/json',
            headers=dict(Authorization=self.get_token())
        )
