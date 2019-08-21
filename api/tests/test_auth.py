# api/tests/test_auth.py


import time
import json
import unittest

from api.v1 import db
from api.v1.models import User, BlacklistToken
from api.tests.base import BaseTestCase

class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ User registration test """

        response = self.register_user(self.registration_data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] ==
                        'You have been successfully registered.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_register_with_registered_email(self):
        """ Test registration for an already registered user """
        user = User(
            name='JonhK',
            email='bettkevin757@gmail.com',
            password='Password@1'
        )
        db.session.add(user)
        db.session.commit()

        response = self.register_user(self.registration_data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed')
        self.assertTrue(
            data['message'] == 'User is already registered. Please log in'
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 202)

    def test_registration_with_invalid_email(self):
        """
        Test where an invalid email is used
        """
        response = self.register_user(self.invalid_email_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == 'Please provide a valid email and try again'
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertTrue(response.status_code, 400)

    def test_invalid_user_name_characters(self):
        """
        Invalid username test
        """
        response = self.register_user(self.invalid_username_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == 'Inalid username. Check and try again.'
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertTrue(response.status_code, 400)

    def test_short_user_name(self):
        """
        Short username test
        """
        response = self.register_user(self.short_username_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == 'Username must have more than 3 characters.'
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_registration_with_invalid_password(self):
        """
        Invalid password test
        """
        response = self.register_user(self.invalid_password_data)
        data = json.loads(response.data.decode())
        self.assertTrue(
            data['message'] == 'Password must be more than 5 characters have one number and symbol'
        )
        self.assertTrue(response.status_code, 400)

    def test_login(self):
        """ Test for login """

        # register user
        reg = self.register_user(self.registration_data)
        reg_data = json.loads(reg.data.decode())
        # login
        response = self.login_user(self.login_data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_wrong_password_login(self):
        reg = self.register_user(self.registration_data)
        reg_data = json.loads(reg.data.decode())

        response = self.login_user(self.wrong_password_data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed')
        self.assertTrue(data['message'] == 'Please check your password and try again')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)


    def test_none_registered_login(self):
        """ Test for none registered login attempt"""

        response = self.login_user(self.login_data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed')
        self.assertTrue(
            data['message'] == 'User does not exist, please sign up'
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertTrue(response.status_code, 404)

    def test_log_out(self):
        # Register
        reg = self.register_user(self.registration_data)
        reg_data = json.loads(reg.data.decode())
        # login
        response = self.login_user(self.login_data)
        data = json.loads(response.data.decode())
        access_token = data['auth_token']
        # logout
        response = self.client.post('/auth/logout', headers=dict(Authorization="Bearer " + access_token),
        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertTrue(result['Message'] == 'you have been successfully logged out')
        self.assertTrue(reg.content_type == 'application/json')

    def test_repeated_log_out(self):
        # Register
        reg = self.register_user(self.registration_data)
        reg_data = json.loads(reg.data.decode())
        # login
        response = self.login_user(self.login_data )
        data = json.loads(response.data.decode())
        access_token = data['auth_token']
        # logout
        response = self.client.post('/auth/logout', headers=dict(Authorization="Bearer " + access_token),
        content_type='application/json')
        response = self.client.post('/auth/logout', headers=dict(Authorization="Bearer " + access_token),
        content_type='application/json')
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == 'You are already looged out.')
        self.assertTrue(reg.content_type == 'application/json')
