import requests
from flask import current_app as app
from .logger import logging


class ServiceCaller:
    SERVICE_ENDPOINTS = {
        "auth": app.config.get("SERVICE_AUTH"),
        "mailer": app.config.get("SERVICE_MAILER")
    }

    ENDPOINTS = {
        "service": {
            "auth": {"version": {"v1": {
                "add_user": "auth/api/v1.0/users/add/user",
                "activate_user_account": "auth/api/v1.0/account",
                "change_user_password": "auth/api/v1.0/users/change/password",
                "get_user": "auth/api/v1.0/users/<id>",
                "get_users": "auth/api/v1.0/users/all",
                "gen_auth_token": "auth/api/v1.0/users/generate/auth/token",
                "validate_auth_token": "auth/api/v1.0/token/validate/token"
            }, "v2": {}}},
            "mailer": {"version": {"v1": {
                "send_email_to_user": "mails/auth/api/v1.0/send/email",
                "send_email_notes_manual_to_all": "mails/api/v1.0/send/notes/manual/to/all"
            }}

            },
            "notes": {

            },
            "schedulers": {

            }
        }
    }

    def __init__(self):
        self.ingress = app.config.get("INGRESS")

    @staticmethod
    def call_endpoint(uri):
        return uri

    @staticmethod
    def service_url(*args):
        return '/'.join(args)

    def call_get_on_service(self, service: str = None, path: str = '', https: bool = True):

        http_protocol = "https:/" if https else "http:/"

        try:
            service = self.SERVICE_ENDPOINTS[service]
        except:
            raise KeyError(f'Provided service value: {service}')

        uri = self.service_url(http_protocol, self.ingress, service, path)
        return requests.get(uri)

    @classmethod
    def call_post_on_service(cls,
                             user_data: dict = None,
                             service: str = None,
                             endpoint: str = '',
                             api_version: str = None,
                             https: bool = True):

        http_protocol = "https:/" if https else "http:/"

        try:
            uri = cls.ENDPOINTS["service"][service]["version"][api_version][endpoint]
        except:
            raise KeyError(f'Provided wrong parameter: service:{service}, api_version:{api_version}')
        return requests.post(cls.service_url(http_protocol, cls.SERVICE_ENDPOINTS[service], uri), json=user_data)

    def call_post_patch_on_service(self):
        pass
