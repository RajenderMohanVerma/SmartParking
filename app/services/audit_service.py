from flask import request
from flask_login import current_user
from app import db
from app.models import ActivityLog

def log_activity(action, target_type=None, target_id=None, details=None, user_id=None):
    try:
        uid = user_id or (current_user.id if current_user and current_user.is_authenticated else None)
        ip = None
        try:
            if request:
                ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        except Exception:
            pass

        entry = ActivityLog(
            user_id=uid,
            action=action,
            target_type=target_type,
            target_id=str(target_id) if target_id else None,
            details=details,
            ip_address=ip
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
