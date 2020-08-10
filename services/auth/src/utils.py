import logging
import uuid
from datetime import datetime

from flask import jsonify

from .models import db, ActivationToken


def generate_uuid4_hex():
    logging.info("auth ::: generate_uuid4_hex ::: get called")
    id = uuid.uuid4()
    return id.hex


def issue_auth_token(user_id):
    logging.info("auth ::: gen_auth_token ::: get called")
    try:
        auth_token = generate_uuid4_hex()

        authorization_token = ActivationToken(token=auth_token,
                                              user_id=user_id,
                                              created_on=datetime.now())
        db.session.add(authorization_token)
        db.session.commit()
        logging.info(f"auth ::: gen_auth_token ::: token: {auth_token} created")
        return True, auth_token
    except Exception as e:
        logging.error(f"auth ::: gen_auth_token ::: {e}")
        return False, jsonify({"code": "404",
                        "msg": f"Error: {e}"})
