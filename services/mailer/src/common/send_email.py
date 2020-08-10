import logging
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from smtplib import SMTP
from ssl import SSLContext, PROTOCOL_TLSv1_2

from flask import current_app as app

from .templates import (email_template_change_password,
                        email_template_renderer_auth,
                        email_template_renderer_repetitions)
from ..models import Notes


class UserMailer:
    MSG_SUBJECTS = {
        "repetitions": "There are some notes to recall",
        "activation": "Activate your account",
        "change_password": "Confirm changing password"
    }

    def __init__(self, content):
        self._topic = None
        self.content = content

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, value):
        if value in self.MSG_SUBJECTS.keys():
            self._topic = value
        else:
            raise KeyError(f'{value}')

    def preapare_email_content(self):
        if self.content['topic'] == 'change_password':
            email_msg_html = email_template_change_password(alternative_id=self.content['alternative_id'],
                                                            activate_token=self.content['auth_token'],
                                                            ingress=app.config.get("INGRESS"))
        elif self.content['topic'] == 'activation':
            email_msg_html = email_template_renderer_auth(alternative_id=self.content['alternative_id'],
                                                          activate_token=self.content['auth_token'],
                                                          ingress=app.config.get("INGRESS"))
        elif self.content['topic'] == 'repetitions':
            data = Notes.get_user_notes_by_user_id(self.content['user_id'])
            email_msg_html = email_template_renderer_repetitions(alternative_id=self.content['alternative_id'],
                                                          data=data,
                                                          ingress=app.config.get("INGRESS"))

        return email_msg_html

    def build_email_msg(self):

        email_msg_html = self.preapare_email_content()

        mail = self.send_email(email=self.content['email'],
                          email_msg_html=email_msg_html,
                          mail_subject=self.MSG_SUBJECTS[self.content['topic']])

        logging.info("mailer ::: send_change_password_email ::: mailed send successfully")

        if mail:
            return True
        else:
            return False

    def send_email(self, email, email_msg_html, display_name='Ryanote', addr_spec=app.config['EMAIL'],
                           mail_subject=""):
        msg = EmailMessage()
        msg['From'] = Address(display_name=display_name, addr_spec=addr_spec)
        msg['To'] = Address(display_name='Sender', addr_spec=email)
        msg['Subject'] = mail_subject

        email_pass = app.config['EMAIL_PASSWORD']

        asparagus_cid = make_msgid()

        msg.set_content(email_msg_html.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

        # Sending the email:
        with SMTP(host='smtp.gmail.com', port=587) as smtp_server:
            if not email_pass:
                raise ValueError(f"Email password value: {email_pass}")

            try:
                # You can choose SSL/TLS encryption protocol to use as shown
                # or just call starttls() without parameters
                smtp_server.starttls(context=SSLContext(PROTOCOL_TLSv1_2))
                smtp_server.login(user='ryanote.reminder@gmail.com', password=email_pass)
                smtp_server.send_message(msg)

            except Exception as e:
                return False
        return True


def multi_send_send_email(email, email_msg_html, display_name='Ryanote', addr_spec=app.config['EMAIL'],
                       mail_subject=""):
    msg = EmailMessage()
    msg['From'] = Address(display_name=display_name, addr_spec=addr_spec)
    msg['To'] = Address(display_name='Sender', addr_spec=email)
    msg['Subject'] = mail_subject

    email_pass = app.config['EMAIL_PASSWORD']

    asparagus_cid = make_msgid()

    msg.set_content(email_msg_html.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

    # Sending the email:
    with SMTP(host='smtp.gmail.com', port=587) as smtp_server:
        if not email_pass:
            raise ValueError(f"Email password value: {email_pass}")

        try:
            # You can choose SSL/TLS encryption protocol to use as shown
            # or just call starttls() without parameters
            smtp_server.starttls(context=SSLContext(PROTOCOL_TLSv1_2))
            smtp_server.login(user='ryanote.reminder@gmail.com', password=email_pass)
            smtp_server.send_message(msg)

        except Exception as e:
            return False
    return True
