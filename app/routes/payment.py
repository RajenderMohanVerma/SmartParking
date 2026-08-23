from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from app.models import Booking, Payment

payment_bp = Blueprint("payment", __name__)


@payment_bp.get("")
@login_required
def index():
    if current_user.role == "ADMIN":
        return redirect(url_for("admin.payments"))
    payments = (
        Payment.query.join(Booking, Payment.booking_id == Booking.id)
        .filter(Booking.user_id == current_user.id)
        .options(joinedload(Payment.booking))
        .order_by(Payment.created_at.desc())
        .all()
    )
    return render_template("user/payments.html", payments=payments)
