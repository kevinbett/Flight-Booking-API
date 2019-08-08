# api/v1/models.py

import jwt
import datetime

from api.v1 import app, db, bcrypt

class User(db.Model):
    """User Model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    reg_date = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, name, password, admin=False):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.reg_date = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        self.admin = admin

    def encode_auth_token(self, user_id):
        """Generate Auth Token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validating auth token
        :param auth_token:
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired'
        except jwt.InvalidTokenError:
            return 'Invalid Token'

    def save(self):
        db.session.add(self)
        db.session.commit()


class BlacklistToken(db.Model):
    """
    Blacklisted Tokens Check
    """
    __tablename__ = "blacklist_tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def save(self):
        db.session.add(self)
        db.session.commit()


class Flight(db.Model):
    """
    Flights Model
    """
    __tablename__ = "flight"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)

    def __init__(self, name, origin, destination, date, departure_time, arrival_time):
        self.name = name
        self.origin = origin,
        self.destination = destination,
        self.date = date,
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def save(self):
        db.session.add(self)
        db.session.commit()


class Image(db.Model):
    """
    Model to store image urls
    """
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(500))
    user = db.Column(db.Integer, db.ForeignKey(User.id))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Return image instance
        """
        return "<Image: {}>".format(self.image_url)
