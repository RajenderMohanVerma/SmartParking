from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import Booking, Notification, ParkingSlot, Vehicle

user_bp = Blueprint("user", __name__)


@user_bp.get("/dashboard")
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("user/dashboard.html", bookings=bookings, available_slots=ParkingSlot.query.filter_by(status="AVAILABLE").count())


@user_bp.route("/vehicles", methods=["GET", "POST"])
@login_required
def vehicles():
    if request.method == "POST":
        number = request.form.get("vehicle_number", "").strip().upper()
        if not number or Vehicle.query.filter_by(vehicle_number=number).first():
            flash("Enter a unique vehicle registration number.", "danger")
        else:
            if request.form.get("is_default"):
                Vehicle.query.filter_by(user_id=current_user.id).update({"is_default": False})
            db.session.add(Vehicle(user_id=current_user.id, vehicle_number=number, vehicle_type=request.form.get("vehicle_type", "Car"), brand=request.form.get("brand"), model=request.form.get("model"), color=request.form.get("color"), fuel_type=request.form.get("fuel_type"), is_default=bool(request.form.get("is_default"))))
            db.session.commit()
            flash("Vehicle added.", "success")
            return redirect(url_for("user.vehicles"))
    return render_template("user/vehicles.html", vehicles=current_user.vehicles)


@user_bp.post("/vehicles/<int:vehicle_id>/default")
@login_required
def set_default_vehicle(vehicle_id):
    vehicle = db.get_or_404(Vehicle, vehicle_id)
    if vehicle.user_id != current_user.id:
        return "Forbidden", 403
    Vehicle.query.filter_by(user_id=current_user.id).update({"is_default": False})
    vehicle.is_default = True
    db.session.commit()
    flash(f"{vehicle.vehicle_number} is now your default vehicle.", "success")
    return redirect(url_for("user.vehicles"))


@user_bp.post("/vehicles/<int:vehicle_id>/delete")
@login_required
def delete_vehicle(vehicle_id):
    vehicle = db.get_or_404(Vehicle, vehicle_id)
    if vehicle.user_id != current_user.id:
        return "Forbidden", 403
    if vehicle.bookings:
        flash("This vehicle has booking history and cannot be deleted.", "warning")
    else:
        db.session.delete(vehicle)
        db.session.commit()
        flash("Vehicle removed from your garage.", "success")
    return redirect(url_for("user.vehicles"))


@user_bp.get("/notifications")
@login_required
def notifications():
    items = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template("user/notifications.html", notifications=items)


@user_bp.post("/notifications/read-all")
@login_required
def read_all():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({"is_read": True})
    db.session.commit()
    return redirect(url_for("user.notifications"))
