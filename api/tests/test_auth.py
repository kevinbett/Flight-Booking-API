# api/tests/test_auth.py


import time
import json
import unittest

from api.v1 import db
from api.v1.models import User, BlacklistToken
from api.tests.base import BaseTestCase


def register_user(self, name, email, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            name=name,
            email=email,
            password=password
        )),
        content_type='application/json'
    )


def login_user(self, email, password):
    return self.client.post(
        'auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):
    # TODO: Rename test case

    def test_registration(self):
        """ User registration test """
        with self.client:
            response = register_user(self, 'Kevin Bett', 'bettkevin757@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] ==
                            'You have been successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_register_with_registered_email(self):
        """ Test registration for an already registered user """
        user = User(
            name='Jonh K',
            email='bettkevin757@gmail.com',
            password='123456'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = register_user(self, 'John K', 'bettkevin757@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(
                data['message'] == 'User is already registered. Please log in'
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_login(self):
        """ Test for login """
        with self.client:
            # register user
            reg = register_user(self, 'Kevin Bett', 'bettkevin757@gmail.com', '123456')
            reg_data = json.loads(reg.data.decode())
            self.assertTrue(reg_data['status'] == 'success')
            self.assertTrue(
                reg_data['message'] == 'You have been successfully registered.'
            )
            self.assertTrue(reg_data['auth_token'])
            self.assertTrue(reg.content_type == 'application/json')
            self.assertEqual(reg.status_code, 201)
            # login
            response = login_user(self, 'bettkevin757@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_none_registered_login(self):
        """ Test for none registered login attempt"""
        with self.client:
            response = login_user(self, 'bett@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(
                data['message'] == 'User does not exist, please sign up'
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(response.status_code, 404)
