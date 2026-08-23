from app import db
from app.models import Notification
from app.services.email_service import send_email


def notify(user_id, title, message, notification_type="INFO", link=None, email=None):
    db.session.add(
        Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            link=link,
        )
    )
    if email:
        send_email(title, email, message)
