# manage.py


import os
import unittest

from flask_apscheduler import APScheduler
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail

from flask_heroku import Heroku

from api.v1 import app, db, models

migrate = Migrate(app, db)
manager = Manager(app)
mail = Mail()
heroku = Heroku(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    mail.init_app(app)
    manager.run()
