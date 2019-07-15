from flask_testing import TestCase

from api.v1 import app, db

class BaseTestCase(TestCase):
    """Base Test"""

    def create_app(self):
        app.config.from_object('api.v1.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
