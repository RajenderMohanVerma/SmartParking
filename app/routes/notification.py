from flask import Blueprint, redirect, url_for
from flask_login import login_required

notification_bp = Blueprint("notification", __name__)


@notification_bp.get("")
@login_required
def index():
    return redirect(url_for("user.notifications"))
