from jinja2 import Template


def email_template_change_password(alternative_id, activate_token, ingress):
    html_email = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
            <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0 "/>
        </head>
        <body>
        <pre>G'day mate !<br/><br/>You told us you forgot your password. If you really did, click here to choose a new one:<br/><br/><a
                href="http://{{ingress}}/notes/account/new/password/{{alternative_id}}/{{activate_token}}">Choose a new password</a></pre>
                <pre>If you didn't mean to reset your password, then you can just ignore this email
                you password will not change.</pre>
        <p>Have a good one,</p>
        <p>Ryanote Team</p>
        </body>
        </html>
    """
    html_email_msg = Template(html_email)
    return html_email_msg.render(alternative_id=alternative_id, activate_token=activate_token, ingress=ingress)


def email_template_renderer_auth(alternative_id, activate_token, ingress):
    html_email = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
            <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0 "/>
        </head>
        <body>
        <pre>G'day mate !<br/><br/>Thank You for registering. To activate your account, please click on the following link (this will confirm your email address)<br/><br/><a
                href="http://{{ingress}}/notes/account/{{alternative_id}}/{{activate_token}}">Activation link</a></pre>
        <p>Have a good one,</p>
        <p>Ryanote Team</p>
        </body>
        </html>
    """
    html_email_msg = Template(html_email)
    return html_email_msg.render(alternative_id=alternative_id, activate_token=activate_token, ingress=ingress)


def email_template_renderer_repetitions(alternative_id, data, ingress):
    html_email = """


    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Demystifying Email Design</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin: 0; padding: 0;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%"> 
        <tr>
            <td style="padding: 10px 0 30px 0;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="500" style="border: 1px solid #cccccc; border-collapse: collapse;">
                    <tr>
                        <td font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
                            <img src="https://sfigiel-ryanote.s3.eu-central-1.amazonaws.com/homepage.png" alt="S3 bucket failed" width="500" height="300" style="display: block;" />
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 16px;">
                                        <b>기억해야 할 몇 가지 메모가 있습니다</b>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td width="300" valign="top">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                        {% for value in data %}
                                                        <tr>
                                                            <td style="padding: 5px 0 0 0; color: #153643; font-family: Arial, sans-serif; font-size: 12px; line-height: 20px;">
                                                                <h4><a href="http://{{ingress}}/notes/get/{{value.id}}/{{value.topic}}">{{value.topic}}</a> ({{value.subject}})</h4>
                                                            </td>
                                                        </tr>
                                                        {% endfor %}
                                                    </table>
                                                </td>
                                                <td style="font-size: 0; line-height: 0;" width="20">
                                                    &nbsp;
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ee4c50" style="padding: 30px 30px 30px 30px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="75%">
                                        &reg; Ryanote 2020<br/>
                                        <a href="#" style="color: #ffffff;"><font color="#ffffff">탈퇴</font></a> 
이 뉴스 레터는 즉시
                                    </td>
                                    <td align="right" width="25%">
                                        <table border="0" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="font-family: Arial, sans-serif; font-size: 12px; font-weight: bold;">
                                                    <a href="http://www.twitter.com/" style="color: #ffffff;">
                                                        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/210284/tw.gif" alt="Twitter" width="38" height="38" style="display: block;" border="0" />
                                                    </a>
                                                </td>
                                                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
                                                <td style="font-family: Arial, sans-serif; font-size: 12px; font-weight: bold;">
                                                    <a href="http://www.facebook.com/" style="color: #ffffff;">
                                                        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/210284/fb.gif" alt="Facebook" width="38" height="38" style="display: block;" border="0" />
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """
    html_email_msg = Template(html_email)
    return html_email_msg.render(alternative_id=alternative_id, data=data, ingress=ingress)


    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <title>Test Email Sample</title>
    #     <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    #     <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    #     <title>Ryanote repetitions</title>
    #     <meta name="viewport" content="width=device-width, initial-scale=1.0 "/>
    # </head>
    # <body>
    # <ol>
    #     {% for value in data %}
    #     <h4><a href="http://{{ingress}}/notes/get/{{value.id}}/{{value.topic}}">{{value.topic}}({{value.subject}})</a></h4>
    #     {% endfor %}
    # </pl>
    # </body>
    # </html>
    # """
