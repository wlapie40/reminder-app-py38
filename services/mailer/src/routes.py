import logging

from flask import current_app as app
from flask import request, jsonify

from .common.send_email import UserMailer
from .common.utils import (query_user_notes,
                           preapare_data_for_sending,
                           send_email_manual_all)


@app.route('/mails/healthcheck', methods=['GET'])
def healthcheck():
    return {"code": "200",
            "msg": "Hello from mailer service"}


@app.route('/mails/auth/api/v1.0/send/email', methods=['POST'])
def send_email_to_user():
    logging.info("mailer ::: send_email_to_user ::: get called")
    content = request.json
    logging.info(f"mailer ::: CONTENT ::: {content}")

    mail_data = UserMailer(content)
    r = mail_data.build_email_msg()

    if r:
        logging.info("mailer ::: send_email_to_user ::: Success")
        return jsonify({"code": "200",
                        "msg": f"Email send"})
    else:
        logging.info("mailer ::: send_email_to_user ::: Error")
        return jsonify({"code": "500",
                        "msg": f"Error"})


@app.route('/mails/api/v1.0/send/notes/manual/to/all', methods=['POST'])
def send_email_notes_manual_to_all():
    logging.info("mailer ::: send_email_notes_manual_to_all ::: get called")
    content = request.json

    user_mail = UserMailer(content)
    user_mail.topic = 'repetitions'

    data = query_user_notes()
    if data:
        data_to_send = preapare_data_for_sending(data)

        user_mail.data_to_send = data_to_send
        result, msg = send_email_manual_all(user_mail, ingress=app.config.get("INGRESS"))

        if result:
            logging.info("mailer ::: send_email_notes_manual_to_all ::: sent successfully")
        else:
            logging.error("mailer ::: send_email_notes_manual_to_all ::: sending mail failed. msg {msg}")
    else:
        logging.info("mailer ::: send_email_notes_manual_to_all ::: no data to send")
    return {"code": "200",
            "msg": ""}

