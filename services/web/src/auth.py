import logging
from datetime import datetime
from datetime import timedelta

from flask import (Blueprint,
                   redirect,
                   render_template,
                   flash,
                   request,
                   url_for)
from flask_login import current_user, login_user

from . import login_manager
from .common.url import ServiceCaller
from .forms import LoginForm, SignupForm
from .models import (db,
                     Users)

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Users.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/notes/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """
    if current_user.is_authenticated:
        logging.info(f'User authenticated')
        return redirect(url_for('get_all_notes', alt_id=current_user.alternative_id))  # Bypass if user is logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        logging.info(f'USER:{user}')
        if user and user.check_password(password=form.password.data):
            logging.info(f'user_{user.id}-{user.username} is logging')
            user.last_login = datetime.now()
            db.session.commit()
            logging.info(f'last_login has been updated')
            login_user(user, remember=True, duration=timedelta(days=1))
            next_page = request.args.get('next')
            return redirect(next_page or url_for('get_all_notes', alt_id=user.alternative_id))
        flash('Invalid email/password combination')
        logging.info(f'WRONG CREDS !!! {form.email.data} was provided')
        return redirect(url_for('auth_bp.login'))
    return render_template('login.html',
                           form=form,
                           title='Log in.',
                           template='login-page',
                           body="Log in with your User account.")


@auth_bp.route('/notes/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up form to create new user accounts.

    GET: Serve sign-up page.
    POST: Validate form, create account, redirect user to dashboard.
    """
    form = SignupForm()
    logging.info('web ::: signup ::: get called')
    if form.validate_on_submit():
        logging.info('web ::: form validated properly')
        existing_user = Users.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            url = ServiceCaller()
            user = {
                "email": form.email.data,
                "username": form.username.data,
                "password": form.password.data}
            logging.info(f'web ::: calling service auth ::: add_user')
            r = url.call_post_on_service(user_data=user,
                                               service="auth",
                                               endpoint="add_user",
                                               api_version="v1",
                                               https=False)
            # user created
            if r.json()["code"] == "201":
                flash(f"""{form.username.data} activate your account to finish signing up.
                We have sent you a welcome email with an activation link to {form.email.data}. \n
                The activation link would stay active for 15 minutes.""")

                return redirect(url_for('auth_bp.login'))
            else:
                flash("Signup failed")
                return redirect(url_for('auth_bp.login'))
        flash('A user already exists with that email address.')
    return render_template('signup.html',
                           title='Create an Account.',
                           form=form,
                           template='signup-page',
                           body="Sign up for a user account.")

