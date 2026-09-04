from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import Booking, FavoriteArea, Notification, ParkingArea, ParkingSlot, Payment, Vehicle

user_bp = Blueprint("user", __name__)


@user_bp.get("/dashboard")
@login_required
def dashboard():
    # Admins should never land on the user dashboard
    if current_user.role == "ADMIN":
        return redirect(url_for("admin.dashboard"))

    status = request.args.get("status", "").strip().upper()
    query = Booking.query.filter_by(user_id=current_user.id)
    if status:
        query = query.filter_by(status=status)
    bookings = query.order_by(Booking.created_at.desc()).all()

    # active session (if any)
    active_booking = Booking.query.filter_by(
        user_id=current_user.id, status="ACTIVE"
    ).first()

    # total amount paid by this user
    total_spent = db.session.query(
        func.coalesce(func.sum(Payment.amount), 0)
    ).join(Booking, Payment.booking_id == Booking.id).filter(
        Booking.user_id == current_user.id,
        Payment.status == "PAID"
    ).scalar() or 0

    # counts for each status
    status_counts = dict(
        db.session.query(Booking.status, func.count(Booking.id))
        .filter(Booking.user_id == current_user.id)
        .group_by(Booking.status)
        .all()
    )

    return render_template(
        "user/dashboard.html",
        bookings=bookings,
        available_slots=ParkingSlot.query.filter_by(status="AVAILABLE").count(),
        status_filter=status,
        active_booking=active_booking,
        total_spent=total_spent,
        status_counts=status_counts,
    )


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
            db.session.add(
                Vehicle(
                    user_id=current_user.id,
                    vehicle_number=number,
                    vehicle_type=request.form.get("vehicle_type", "Car"),
                    brand=request.form.get("brand"),
                    model=request.form.get("model"),
                    color=request.form.get("color"),
                    fuel_type=request.form.get("fuel_type"),
                    is_default=bool(request.form.get("is_default")),
                )
            )
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


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        if not full_name:
            flash("Full name is required.", "danger")
        else:
            current_user.full_name = full_name
            current_user.phone = phone or None
            current_user.address = address or None
            db.session.commit()
            flash("Profile updated.", "success")
            return redirect(url_for("user.profile"))
    return render_template("user/profile.html")


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


@user_bp.post("/notifications/<int:notification_id>/read")
@login_required
def read_one(notification_id):
    item = db.get_or_404(Notification, notification_id)
    if item.user_id != current_user.id:
        return "Forbidden", 403
    item.is_read = True
    db.session.commit()
    if item.link:
        return redirect(item.link)
    return redirect(url_for("user.notifications"))


@user_bp.post("/favorites/<int:area_id>/toggle")
@login_required
def toggle_favorite(area_id):
    area = db.get_or_404(ParkingArea, area_id)
    fav = FavoriteArea.query.filter_by(user_id=current_user.id, area_id=area.id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        flash(f"Removed {area.name} from your favorites.", "info")
    else:
        db.session.add(FavoriteArea(user_id=current_user.id, area_id=area.id))
        db.session.commit()
        flash(f"Added {area.name} to your favorites!", "success")
    
    referrer = request.referrer
    if referrer and "/parking" in referrer:
        return redirect(referrer)
    return redirect(url_for("parking.index"))

