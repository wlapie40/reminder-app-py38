from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     DateField,
                     SelectField,
                     PasswordField,
                     ValidationError)
from flask_ckeditor import CKEditorField
from wtforms.validators import (DataRequired,
                                EqualTo,
                                Length)

from .models import Notes, Users
from datetime import date


class NewNoteForm(FlaskForm):
    topic = StringField('Topic', validators=[Length(max=80,
                                                    message='80 characters is the maximum length.'),
                                             DataRequired()])
    subject = SelectField('Subject', validators=[DataRequired()],
                        choices=[('English', 'English'),
                                 ('Python', 'Python'),
                                 ('Kubernetes', 'Kubernetes'),
                                 ('Other', 'Other')])
    url = StringField('URL')
    text = CKEditorField('Text')
    created = DateField('Created', default=date.today())
    repeat_at = DateField('Repeat_at')
    submit = SubmitField('Add a new note')

    def validate_topic(self, topic):
        note = Notes.query.filter_by(topic=topic.data).first()
        if note is not None:
            raise ValidationError('Topic already exists.')

    # def validate_url(self, url):
    #     url = Notes.query.filter_by(url=url.data).first()
    #     if url is not None:
    #         raise ValidationError('Url already exists.')
    #     if len(str(url)) > 420:
    #         raise ValidationError('Url longer than 420 characters')


class EditNoteForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    # subject = SelectField('Subject', validators=[DataRequired()],
    #                     choices=[('English', 'English'),
    #                              ('Python', 'Python'),
    #                              ('Kubernetes', 'Kubernetes'),
    #                              ('Other', 'Other')])
    subject = StringField('Subject')
    url = StringField('URL')
    text = TextAreaField('Text')
    created = DateField('Created', default=date.today())
    repeat_at = DateField('Repeat_at')
    submit = SubmitField('Add a new note')


class SignupForm(FlaskForm):
    """User Signup Form."""
    username = StringField('Username',
                       validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Length(min=6), DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(f'Username {user.username} already exists')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(f'Email: {user.email} is being used by another user')
        if email in ["wlapie40@gmail.com", "szymon.figiel@outlook.com", "ryan_89@gmail.com"]:
            raise ValidationError(f'Email not authorized')


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(f'Email: "{email.data}" has not been found')
        if not user.account_activated:
            raise ValidationError(f'Email has not been activated')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Log In')
    recaptcha = RecaptchaField()

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(f'There is no account related with: {email.data}')


class ChangePasswordForm(FlaskForm):
    submit = SubmitField('Log In')
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    recaptcha = RecaptchaField()

    # def validate_email(self, email):
    #     user = Users.query.filter_by(email=email.data).first()
    #     if not user:
    #         raise ValidationError(f'There is no account related with: {email.data}')