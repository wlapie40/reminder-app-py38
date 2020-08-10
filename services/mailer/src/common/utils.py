import collections
import uuid
from datetime import date

from jinja2 import Template
from src.models import db, Notes, Users

from .logger import logging
# from .send_email import send_email
from .send_email import multi_send_send_email


def generate_uuid4_hex():
    id = uuid.uuid4()
    return id.hex


# todo create a generalic lass with templates
def email_template_renderer(data, ingress):
    html_email = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Email Sample</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0 "/>
        <style>
    <!--- CSS code (if any) --->

        </style>
    </head>
    <body>
    <ul>
        {% for value in data %}
        <h4><a href="http://{{ingress}}/notes/get/{{value[0]}}/{{value[1]}}">{{value[1]}}</a></h4>
        <li>Subject: {{value[4]}}</li>
        <li>Text: {{value[2]}}</li>
        <li>URL: <a href="{{value[3]}}">LINK</a></li>
        <br>
        {% endfor %}
    </ul>
    </body>
    </html>
    """
    html_email_msg = Template(html_email)
    return html_email_msg.render(data=data, ingress=ingress)

#
# def send_auth_mail(alternative_id, auth_token, user_email, subject):
#     email_msg_html = email_template_renderer_auth_test(alternative_id,
#                                                        auth_token,
#                                                        ingress=app.config.get("INGRESS"))
#     send_email_to_user(user_email, email_msg_html, subject)
#     return True


def send_email_manual_all(user_mail, ingress):
    # try:
    logging.info("mailer ::: send_email_manual_all ::: called")
    # todo write a separate function to process email msg's
    mail_subject = user_mail.topic
    for el in user_mail.data_to_send.items():
        email_to_send = el[0]
        logging.info(f"mailer ::: send_email_manual_all ::: send to: {email_to_send}")
        data = el[1]
        email_msg_html = email_template_renderer(data, ingress)

        multi_send_send_email(str(email_to_send),
                           email_msg_html,
                           mail_subject=user_mail.MSG_SUBJECTS[mail_subject])
    logging.info("mailer ::: send_email_manual_all ::: mail sent")
    return True, "success"


def preapare_data_for_sending(data):
    try:
        logging.info("mailer ::: PREAPARE_DATA_FOR_SENDING ::: called")
        dict_x = collections.defaultdict(list)
        for el in data:
            dict_x.setdefault(el.Users.email, []).append([el.Notes.id,
                                                          el.Notes.topic,
                                                          el.Notes.text,
                                                          el.Notes.url,
                                                          el.Notes.subject,
                                                          el.Users.username])
        logging.info(f"mailer ::: PREAPARE_DATA_FOR_SENDING ::: dict_x: {dict_x}")
        return dict_x
    except Exception as msg:
        logging.error(f"mailer ::: PREAPARE_DATA_FOR_SENDING ::: ERROR {msg}")


def get_date_today():
    return date.today()


def query_user_notes():
    logging.info("mailer ::: QUERY_USER_NOTES ::: called")
    try:
        return db.session.query(Notes, Users). \
            join(Users, Users.id == Notes.user_id). \
            filter(Notes.repeat_at <= get_date_today()).all()
    except Exception as msg:
        logging.error(f"mailer ::: QUERY_USER_NOTES ::: QUERY ERROR {msg}")
        return False
