from flask_login import UserMixin
from werkzeug.security import (generate_password_hash,
                               check_password_hash)

from . import db


class Notes(db.Model):
    """Data model for user notes."""

    __tablename__ = 'notes'
    id = db.Column(db.Integer,
                   primary_key=True)
    topic = db.Column(db.String(80),
                        index=False,
                        unique=True,
                        nullable=False)
    url = db.Column(db.String(420),
                         index=False,
                         unique=False,
                         nullable=True)
    subject = db.Column(db.String(80),
                        index=False,
                        unique=False,
                        nullable=False)
    text = db.Column(db.Text,
                         index=False,
                         unique=False,
                         nullable=True)
    learned = db.Column(db.Boolean,
                        default=True,
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    created = db.Column(db.Date,
                        index=False,
                        unique=False,
                        nullable=False)
    repeat_at = db.Column(db.Date,
                        index=False,
                        unique=False,
                        nullable=False)

    @classmethod
    def get_user_notes(cls, user: str, note_id=None):
        if note_id:
            return db.session.query(cls).\
                filter(cls.user_id == user)\
                .filter(cls.id == note_id).first()
        else:
            return db.session.query(cls)\
                .filter(cls.user_id == user)\
                .order_by(cls.repeat_at.asc()).all()

    @classmethod
    def get_user_note_by_id(cls, note_id: str):
        return db.session.query(cls).\
                filter(cls.id == note_id).first()

    def __repr__(self):
        return '<Notes {}, {}, {}, {}>'.format(self.topic,
                                            self.subject,
                                            self.created,
                                            self.repeat_at)


class Users(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'users'
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
    notes = db.relationship('Notes',
                            backref='users',
                            lazy=True)
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

    def __repr__(self):
        return '<User {}>'.format(self.username)


class ActivationToken(db.Model):
    """Data model for user notes."""

    __tablename__ = 'activation_token'
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
