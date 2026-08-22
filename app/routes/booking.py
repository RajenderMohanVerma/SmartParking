from datetime import datetime, timezone
import uuid

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Booking, ParkingSlot, Pricing, Vehicle
from app.services.fee_service import calculate_fee
from app.services.notification_service import notify
from app.services.pdf_service import receipt_pdf
from app.services.qr_service import make_qr

booking_bp = Blueprint("booking", __name__)


def parse_datetime(value):
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def as_utc(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def expire_reservations():
    cutoff = datetime.now(timezone.utc)
    changed = False
    for booking in Booking.query.filter_by(status="CONFIRMED").all():
        entry_time = as_utc(booking.entry_time)
        if entry_time < cutoff and (cutoff - entry_time).total_seconds() > 30 * 60:
            booking.status = "EXPIRED"
            booking.slot.status = "AVAILABLE"
            notify(booking.user_id, "Booking expired", f"Booking {booking.booking_id} expired before arrival.", "BOOKING")
            changed = True
    if changed:
        db.session.commit()


@booking_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    expire_reservations()
    slots = ParkingSlot.query.filter_by(status="AVAILABLE").all()
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        try:
            slot_id = int(request.form.get("slot_id", "0"))
            vehicle_id = int(request.form.get("vehicle_id", "0"))
        except (TypeError, ValueError):
            slot_id = vehicle_id = 0
        slot = db.session.get(ParkingSlot, slot_id)
        vehicle = db.session.get(Vehicle, vehicle_id)
        try:
            entry = parse_datetime(request.form["entry_time"])
            exit_time = parse_datetime(request.form["expected_exit_time"])
        except (KeyError, ValueError):
            flash("Use valid entry and exit times.", "danger")
            return render_template("booking/new.html", slots=slots, vehicles=vehicles, selected_slot_id=slot_id)
        if not slot or slot.status != "AVAILABLE" or not vehicle or vehicle.user_id != current_user.id or exit_time <= entry:
            flash("That slot is no longer available or the booking details are invalid.", "danger")
        else:
            pricing = Pricing.query.filter_by(is_active=True).first() or Pricing(name="Default")
            if pricing.id is None:
                db.session.add(pricing)
                db.session.flush()
            slot.status = "RESERVED"
            booking = Booking(booking_id=f"SP-{datetime.now().year}-{uuid.uuid4().hex[:8].upper()}", user_id=current_user.id, vehicle_id=vehicle.id, parking_area_id=slot.area_id, parking_slot_id=slot.id, booking_date=entry.date(), entry_time=entry, expected_exit_time=exit_time, estimated_fee=calculate_fee(entry, exit_time, pricing))
            db.session.add(booking)
            db.session.flush()
            notify(current_user.id, "Booking confirmed", f"Your slot {slot.slot_number} is reserved.", "BOOKING")
            db.session.commit()
            flash(f"Booking {booking.booking_id} confirmed.", "success")
            return redirect(url_for("user.dashboard"))
    selected_slot_id = request.args.get("slot_id", type=int)
    return render_template("booking/new.html", slots=slots, vehicles=vehicles, selected_slot_id=selected_slot_id)


@booking_bp.get("/<int:booking_id>")
@login_required
def detail(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != current_user.id and current_user.role != "ADMIN":
        return "Forbidden", 403
    return render_template("booking/detail.html", booking=booking)


@booking_bp.get("/<int:booking_id>/qr")
@login_required
def qr(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != current_user.id and current_user.role != "ADMIN":
        return "Forbidden", 403
    return send_file(make_qr(booking.qr_token), mimetype="image/png", download_name=f"{booking.booking_id}.png")


@booking_bp.get("/<int:booking_id>/receipt")
@login_required
def receipt(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != current_user.id and current_user.role != "ADMIN":
        return "Forbidden", 403
    return send_file(receipt_pdf(booking), mimetype="application/pdf", as_attachment=True, download_name=f"{booking.booking_id}-receipt.pdf")


@booking_bp.post("/<int:booking_id>/cancel")
@login_required
def cancel(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != current_user.id and current_user.role != "ADMIN":
        return "Forbidden", 403
    if booking.status == "CONFIRMED":
        booking.status = "CANCELLED"
        booking.slot.status = "AVAILABLE"
        notify(booking.user_id, "Booking cancelled", f"Booking {booking.booking_id} has been cancelled.", "BOOKING")
        db.session.commit()
        flash("Booking cancelled and slot released.", "success")
    else:
        flash("Only confirmed bookings can be cancelled.", "warning")
    return redirect(url_for("booking.detail", booking_id=booking.id))
