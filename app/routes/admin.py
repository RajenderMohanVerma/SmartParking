from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import Booking, ParkingArea, ParkingSlot, Payment, User
from app.services.notification_service import notify
import uuid
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/dashboard")
@login_required
@admin_required
def dashboard():
    stats = {"users": User.query.count(), "areas": ParkingArea.query.count(), "slots": ParkingSlot.query.count(), "available": ParkingSlot.query.filter_by(status="AVAILABLE").count(), "reserved": ParkingSlot.query.filter_by(status="RESERVED").count(), "active": Booking.query.filter_by(status="ACTIVE").count()}
    return render_template("admin/dashboard.html", stats=stats, bookings=Booking.query.order_by(Booking.created_at.desc()).limit(10).all())


@admin_bp.get("/users")
@login_required
@admin_required
def users():
    search = request.args.get("q", "").strip()
    query = User.query
    if search:
        query = query.filter((User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))
    return render_template("admin/users.html", users=query.order_by(User.created_at.desc()).all())


@admin_bp.post("/users/<int:user_id>/toggle")
@login_required
@admin_required
def toggle_user(user_id):
    user = db.get_or_404(User, user_id)
    if user.id == 1 or user.id == current_user.id:
        flash("This account cannot be deactivated.", "warning")
    else:
        user.is_active = not user.is_active
        db.session.commit()
        flash("User status updated.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/areas", methods=["GET", "POST"])
@login_required
@admin_required
def areas():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        if not name or not location:
            flash("Area name and location are required.", "danger")
        elif ParkingArea.query.filter_by(name=name).first():
            flash("An area with that name already exists.", "danger")
        else:
            db.session.add(ParkingArea(name=name, location=location, operating_hours=request.form.get("operating_hours") or "Open 24 hours"))
            db.session.commit()
            flash("Parking area created.", "success")
            return redirect(url_for("admin.areas"))
    return render_template("admin/areas.html", areas=ParkingArea.query.order_by(ParkingArea.name).all())


@admin_bp.post("/bookings/<int:booking_id>/check-in")
@login_required
@admin_required
def check_in(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.status != "CONFIRMED":
        flash("Only confirmed bookings can check in.", "danger")
    else:
        booking.status = "ACTIVE"
        booking.actual_entry_time = datetime.now(timezone.utc)
        booking.slot.status = "OCCUPIED"
        db.session.commit()
        flash("Vehicle checked in.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.post("/bookings/<int:booking_id>/check-out")
@login_required
@admin_required
def check_out(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.status != "ACTIVE":
        flash("Only active bookings can check out.", "danger")
    else:
        booking.status = "COMPLETED"
        booking.actual_exit_time = datetime.now(timezone.utc)
        booking.final_fee = booking.estimated_fee
        booking.slot.status = "AVAILABLE"
        db.session.add(Payment(transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}", booking_id=booking.id, amount=booking.final_fee, payment_method="Cash", status="PAID"))
        notify(booking.user_id, "Payment completed", f"Your parking payment for {booking.booking_id} is complete.", "PAYMENT")
        db.session.commit()
        flash("Vehicle checked out and slot released.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/verify", methods=["GET", "POST"])
@login_required
@admin_required
def verify():
    booking = None
    message = None
    if request.method == "POST":
        token = request.form.get("qr_token", "").strip()
        booking = Booking.query.filter_by(qr_token=token).first() or Booking.query.filter_by(booking_id=token).first()
        if not booking:
            message = "Invalid QR reference or booking ID."
        elif booking.status != "CONFIRMED":
            message = f"Booking is {booking.status.lower()} and cannot check in."
    return render_template("admin/verify.html", booking=booking, message=message)
