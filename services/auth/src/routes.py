import logging
from datetime import datetime, timedelta

from flask import current_app as app
from flask import request, redirect, url_for, jsonify, flash

from .models import db, Users, ActivationToken
from .url import ServiceCaller
from .utils import generate_uuid4_hex, issue_auth_token

ENDPOINTS = {
    "add_user": "/auth/api/v1.0/users/add/user",
    "gen_auth_token": "/auth/api/v1.0/users/generate/auth/token",
    "endpoints": "/auth/endpoints",
    "get_user": "/auth/api/v1.0/users/<id>",
    "get_users": "/auth/api/v1.0/users/all",
    "get_tokens": "/auth/api/v1.0/tokens/all",
    "healthcheck": "/auth/healthcheck",
    "remove_user": "/auth/api/v1.0/users/remove/user/<id>",
    "remove_token": "/auth/api/v1.0/token/remove/token",
    "send_email_to_user": "/mails/auth/api/v1.0/send/email",
    "validate_auth_token": "/auth/api/v1.0/token/validate/token"
}


@app.route('/auth/api/v1.0/account', methods=['POST'])
def activate_user_account():
    logging.info(f'auth ::: activate_user_account ::: get called')
    content = request.json

    user = Users.query.filter_by(alternative_id=content['alternative_id']).first()
    if not user:
        flash('Account activation failed')
        return redirect(url_for('auth_bp.login'))

    q = db.session.query(Users, ActivationToken) \
        .join(Users, Users.id == user.id) \
        .filter(ActivationToken.token == content['activate_token']) \
        .filter(ActivationToken.user_id == user.id).first()

    if q:
        q.Users.account_activated = True
        token = ActivationToken.query.filter_by(token=content['activate_token']).first()
        db.session.delete(token)
        db.session.commit()
        logging.info(f'auth ::: activate_user_account ::: Auth token deleted')
        logging.info(f'auth ::: activate_user_account ::: Account {q.Users.alternative_id} activated')
        flash('Account activated successfully')

        return jsonify({"code": "201",
                        "msg": f"New user account activated"})

    return jsonify({"code": "500",
                    "msg": "Error"})


@app.route(ENDPOINTS['add_user'], methods=['POST'])
def add_user():
    logging.info('auth ::: add_user ::: get called')
    content = request.json

    alternative_id = generate_uuid4_hex()
    logging.info(f'auth ::: add_user ::: alternative_id: {alternative_id}')

    user = Users(
        alternative_id=alternative_id,
        created_on=datetime.now(),
        email=content['email'],
        username=content['username'])
    user.set_password(content['password'])
    db.session.add(user)
    db.session.commit()
    logging.info(f'auth ::: add_user ::: user: {content["username"]} added')

    status, result = issue_auth_token(user.id)

    if status:
        # send an activation e-mail to user
        url = ServiceCaller()
        user_data = {
            'alternative_id': alternative_id,
            'auth_token': result,
            'email': content['email'],
            'topic': 'activation'
        }

        r = url.call_post_on_service(user_data=user_data,
                                     service="mailer",
                                     endpoint="send_email_to_user",
                                     api_version="v1",
                                     https=False)

        if r.json()["code"] == "200":
            return jsonify({"code": "201",
                            "msg": f"New has been created.",
                            "alternative_id": alternative_id,
                            "user_id": user.id})
        else:
            return jsonify({"code": "500",
                            "msg": f"Creating new user failed."})
    else:
        logging.error('auth ::: add_user ::: auth token has not been generated')
        return jsonify({"code": "400",
                        "msg": "Error"})


@app.route(ENDPOINTS['gen_auth_token'], methods=['POST'])
def gen_auth_token():
    logging.info("auth ::: gen_auth_token ::: get called")
    content = request.json

    status, auth_token = issue_auth_token(content['user_id'])
    return jsonify({"code": "201",
                    "auth_token": auth_token})


@app.route(ENDPOINTS['endpoints'], methods=['GET'])
def endpoints():
    logging.info(f"auth ::: endpoints ::: get called")
    return jsonify(ENDPOINTS)


@app.route(ENDPOINTS['get_users'], methods=['GET'])
def get_users():
    logging.info(f"auth ::: get_users ::: get called")
    users = Users.query.all()
    return jsonify(users)


@app.route(ENDPOINTS['get_user'], methods=['GET'])
def get_user(id):
    logging.info(f"auth ::: get_user ::: get called")
    user = Users.query.filter_by(id=id).first_or_404()
    if user:
        return jsonify(user)
    else:
        return {"code": 404,
                "msg": f"user with id:{id} not found. Try {ENDPOINTS['get_all_users']} to list all users"}


@app.route(ENDPOINTS['get_tokens'], methods=['GET'])
def get_tokens():
    logging.info(f"auth ::: get_tokens ::: get called")

    tokens = ActivationToken.query.all()
    return jsonify(tokens)


@app.route(ENDPOINTS['healthcheck'], methods=['GET'])
def healthcheck():
    logging.info(f"auth ::: healthcheck ::: get called")
    return {"code": "200",
            "msg": "Hello from auth service"}


@app.route(ENDPOINTS['remove_token'], methods=['POST'])
def remove_token():
    logging.info(f"auth ::: remove_token ::: get called")

    content = request.json
    token_id = content["token_id"]

    logging.info(f"auth ::: remove_token ::: get called with token: {token_id}")

    q = ActivationToken.query.filter(ActivationToken.id == token_id).first()
    if q:
        ActivationToken.query.filter(ActivationToken.id == token_id).delete()
        db.session.commit()
        logging.info(f"auth ::: remove_token ::: token: {token_id} deleted")
        return {"code": "200",
                "msg": "Token deleted"}
    else:
        logging.info(f"auth ::: remove_token ::: Token id:{token_id} not found")
        return {"code": "404",
                "msg": f"Token id:{token_id} not found"}


@app.route(ENDPOINTS['remove_user'], methods=['GET'])
def remove_user(id):
    logging.info(f"auth ::: remove_user ::: get called")

    Users.query.filter(Users.id == id).delete()
    db.session.commit()

    q = Users.query.filter(Users.id == id).first()
    if not q:
        return {"code": "200"}
    else:
        return {"code": "500",
                "msg": f"User id:{id} has not been deleted."}


@app.route(ENDPOINTS['validate_auth_token'], methods=['POST'])
def validate_auth_token():
    logging.info(f"auth ::: validate_auth_token ::: get called")
    # check if activate token is no older than 30 minutes
    content = request.json

    user = Users.query.filter_by(alternative_id=content['alternative_id']).first()

    q = db.session.query(Users, ActivationToken) \
        .join(Users, Users.id == user.id) \
        .filter(ActivationToken.token == content["activate_token"]) \
        .filter(ActivationToken.user_id == user.id).first()
    # todo
    # test = q.ActivationToken.created_on - datetime.now()
    if q:
        user.set_password(content['password'])
        ActivationToken.query.filter_by(user_id=user.id).delete()
        db.session.commit()

        return {"code": "201",
                "msg": "Password changed successfully"}
    else:
        # todo improve these msg
        return {"code": "500",
                "msg": f"User with alternative_id: {content['alternative_id']} not found"}


@app.route("/auth/test", methods=['GET'])
def clear_old_tokens():
    logging.info(f"auth ::: clear_old_tokens ::: get called")

    deprecated_tokens = ActivationToken.query.filter(
        ActivationToken.created_on >= datetime.now() + timedelta(minutes=30)).all()
    test = [el.id for el in deprecated_tokens]
    if deprecated_tokens:
        deleted_objects = ActivationToken.__table__.delete().where(ActivationToken.id.in_(test))
        db.session.execute(deleted_objects)
        db.session.commit()
    return {"code": "200"}
