from app import db
from app.models import Notification


def notify(user_id, title, message, notification_type="INFO"):
    db.session.add(Notification(user_id=user_id, title=title, message=message, type=notification_type))
