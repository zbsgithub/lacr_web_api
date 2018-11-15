# -*- coding: utf-8 -*-
from random import Random
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _


from users.models import EmailVerifyRecord
from b2b.settings import EMAIL_FROM


WELCOME_CONTENT = _(u"Dear Customer:")
ACTIVATE_EMAIL_CONTENT = _(u"Welcome to join IMTGO, please click on the ‘Activate Now’"
                           u" button to complete your activation")
VERIFY_EMAIL_CONTENT = _(u"For the safety of your account, please click on the ‘Verify’ button to verify your identity")
ACTIVATE_BUTTON = _(u"Activate Now")
VERIFY_BUTTON = _(u"Verify")

EMAIL_HTML_CONTENT = u'\
        <!DOCTYPE html>\
        <html lang="en">\
        <head>\
            <meta charset="UTF-8">\
            <title>IMTGO</title>\
            <style type="text/css">\
                div {\
                    padding: 5px 20px;\
                    background: #4d92df;\
                    color: white;\
                }\
                a {\
                    text-decoration: none;\
                    display: block;\
                    width: 100px;\
                    height: 30px;\
                    background: #E75858;\
                    text-align: center;\
                    padding: 2px;\
                    box-sizing: border-box;\
                    color: white;\
                    border-radius: 5px;\
                    box-shadow: 1px 1px 1px red;\
                    line-height: 30px;\
                }\
            </style>\
        </head>\
        <body>\
            <div>\
                <h1>%s</h1>\
                <h2>%s</h2>\
                <a href="%s/%s">%s</a>\
            </div>\
        </body>\
        </html>\
        '


def random_str(random_len=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()

    random_code = ''
    for i in range(random_len):
        random_code += chars[random.randint(0, length)]
    return random_code


def send_register_email(email, page, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(random_len=16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = _(u"Activate IMTGO Account")
        email_content = _(u"Activate IMTGO Account:") + '{0}/{1}'.format(page, code)
        # html_content = _(u"点击连接激活账号:") + '<a href="{0}/{1}">click me</a>'.format(page, code)

        html_content = EMAIL_HTML_CONTENT % (WELCOME_CONTENT, ACTIVATE_EMAIL_CONTENT, page, code, ACTIVATE_BUTTON)

        msg = EmailMultiAlternatives(email_title, email_content, EMAIL_FROM, [email])
        msg.attach_alternative(html_content, "text/html")
        send_status = msg.send()
        if send_status:
            print("send email success", send_status)
            return True, code
        else:
            print("send email failed", send_status)
            return False, None

    elif send_type == "reset":
        email_title = _(u"Reset IMTGO Account")
        email_content = _(u"Reset IMTGO Account:") + '{0}/{1}'.format(page, code)
        # html_content = _(u"点击连接重置密码:") + '<a href="{0}/{1}">click me</a>'.format(page, code)
        # html_content = EMAIL_HTML_CONTENT % (WELCOME_CONTENT, VERIFY_EMAIL_CONTENT, VERIFY_BUTTON, page, code)
        html_content = EMAIL_HTML_CONTENT % (WELCOME_CONTENT, ACTIVATE_EMAIL_CONTENT, page, code, VERIFY_BUTTON)

        msg = EmailMultiAlternatives(email_title, email_content, EMAIL_FROM, [email])
        msg.attach_alternative(html_content, "text/html")
        send_status = msg.send()
        if send_status:
            print("send email success")
            return True, code
        else:
            print("send email failed")
            return False, None
