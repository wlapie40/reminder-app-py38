from flask import current_app as app


@app.route('/mails/healthcheck', methods=['GET'])
def healthcheck_mailer():
    return {"code": "200",
            "msg": "request send from service auth to mailer"}