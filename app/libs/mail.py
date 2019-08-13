from flask_mail import Message

from app import mail


def send_verification_mail(recipient, code):
    msg = Message()
    msg.subject = "验证码"
    msg.recipients = [recipient]
    msg.html = "你的验证码为：{}".format(code)
    mail.send(msg)
