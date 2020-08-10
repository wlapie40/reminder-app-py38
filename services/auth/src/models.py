from flask_login import UserMixin
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from dataclasses import dataclass
from . import db


@dataclass
class Users(UserMixin, db.Model):
    """User account model."""
    __tablename__ = 'users'

    id: int
    alternative_id: str
    username: str
    email: str
    password: str
    account_activated: bool
    created_on: str
    last_login: str

    id = db.Column(db.Integer,
                           primary_key=True)
    alternative_id = db.Column(db.String(32),
                            nullable=False)
    username = db.Column(db.String(100),
                           nullable=False,
                           unique=False)
    email = db.Column(db.String(40),
                           unique=True,
                           nullable=False)
    password = db.Column(db.String(200),
                           primary_key=False,
                           unique=False,
                           nullable=False)
    account_activated = db.Column(db.Boolean,
                           default=False,
                           nullable=False)
    # notes = db.relationship('Notes',
    #                         backref='users',
    #                         lazy=True)
    activation_token = db.relationship('ActivationToken',
                            backref='users',
                            lazy=True)
    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256', salt_length=9)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    # @classmethod
    # def get_all_users(cls):
    #     return db.session.query(cls)\
    #         .order_by(cls.id.asc()).all()

    def __repr__(self):
        return '<User {}>'.format(self.username)


@dataclass
class ActivationToken(db.Model):
    """Data model for user notes."""

    __tablename__ = 'activation_token'

    id: int
    token: str
    user_id: int
    created_on: str

    id = db.Column(db.Integer,
                   primary_key=True)
    token = db.Column(db.String(80),
                        index=False,
                        unique=True,
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    created_on = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)

    def __repr__(self):
        return '<ActivationToken {}, {}, {}>'.format(self.id,
                                            self.token,
                                            self.created_on)
