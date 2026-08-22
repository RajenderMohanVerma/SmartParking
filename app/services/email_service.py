from flask import current_app
from flask_mail import Message

from app import mail


def send_email(subject, recipient, body):
    if not current_app.config.get("MAIL_SERVER") or not recipient:
        return False
    try:
        mail.send(Message(subject=subject, recipients=[recipient], body=body))
        return True
    except Exception:
        current_app.logger.exception("Email delivery failed")
        return False
