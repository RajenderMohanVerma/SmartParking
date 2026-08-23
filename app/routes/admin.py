from datetime import date, datetime, timezone
import uuid

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import Booking, ParkingArea, ParkingSlot, Payment, PaymentPolicy, Pricing, User
from app.services.fee_service import is_user_parking_free, set_setting
from app.services.notification_service import notify
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/dashboard")
@login_required
@admin_required
def dashboard():
    stats = {
        "users": User.query.count(),
        "areas": ParkingArea.query.count(),
        "slots": ParkingSlot.query.count(),
        "available": ParkingSlot.query.filter_by(status="AVAILABLE").count(),
        "reserved": ParkingSlot.query.filter_by(status="RESERVED").count(),
        "active": Booking.query.filter_by(status="ACTIVE").count(),
    }
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        bookings=Booking.query.order_by(Booking.created_at.desc()).limit(10).all(),
        parking_free=is_user_parking_free(),
    )


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
            db.session.add(
                ParkingArea(
                    name=name,
                    location=location,
                    operating_hours=request.form.get("operating_hours") or "Open 24 hours",
                    description=request.form.get("description"),
                    floors=int(request.form.get("floors") or 1),
                )
            )
            db.session.commit()
            flash("Parking area created.", "success")
            return redirect(url_for("admin.areas"))
    return render_template("admin/areas.html", areas=ParkingArea.query.order_by(ParkingArea.name).all())


@admin_bp.post("/areas/<int:area_id>/toggle")
@login_required
@admin_required
def toggle_area(area_id):
    area = db.get_or_404(ParkingArea, area_id)
    area.status = "INACTIVE" if area.status == "ACTIVE" else "ACTIVE"
    db.session.commit()
    flash(f"{area.name} is now {area.status}.", "success")
    return redirect(url_for("admin.areas"))


@admin_bp.route("/slots", methods=["GET", "POST"])
@login_required
@admin_required
def slots():
    areas = ParkingArea.query.order_by(ParkingArea.name).all()
    if request.method == "POST":
        area_id = request.form.get("area_id", type=int)
        slot_number = request.form.get("slot_number", "").strip().upper()
        area = db.session.get(ParkingArea, area_id) if area_id else None
        if not area or not slot_number:
            flash("Area and slot number are required.", "danger")
        elif ParkingSlot.query.filter_by(area_id=area.id, slot_number=slot_number).first():
            flash("That slot number already exists in this area.", "danger")
        else:
            db.session.add(
                ParkingSlot(
                    area_id=area.id,
                    slot_number=slot_number,
                    floor=int(request.form.get("floor") or 1),
                    slot_type=request.form.get("slot_type") or "Normal",
                    vehicle_type=request.form.get("vehicle_type") or "Any",
                    price=float(request.form.get("price") or 0),
                    location_info=request.form.get("location_info"),
                    status="AVAILABLE",
                )
            )
            db.session.commit()
            flash("Slot created.", "success")
            return redirect(url_for("admin.slots"))
    area_filter = request.args.get("area_id", type=int)
    query = ParkingSlot.query.join(ParkingArea)
    if area_filter:
        query = query.filter(ParkingSlot.area_id == area_filter)
    return render_template(
        "admin/slots.html",
        areas=areas,
        slots=query.order_by(ParkingArea.name, ParkingSlot.slot_number).all(),
        area_filter=area_filter,
    )


@admin_bp.post("/slots/<int:slot_id>/update")
@login_required
@admin_required
def update_slot(slot_id):
    slot = db.get_or_404(ParkingSlot, slot_id)
    if slot.bookings and any(b.status in ("CONFIRMED", "ACTIVE") for b in slot.bookings):
        flash("Cannot change a slot with an active reservation. Release it first.", "warning")
        return redirect(url_for("admin.slots"))
    slot.slot_type = request.form.get("slot_type") or slot.slot_type
    slot.vehicle_type = request.form.get("vehicle_type") or slot.vehicle_type
    slot.price = float(request.form.get("price") or 0)
    slot.floor = int(request.form.get("floor") or slot.floor)
    status = request.form.get("status")
    if status in ("AVAILABLE", "OCCUPIED", "RESERVED", "MAINTENANCE"):
        slot.status = status
    db.session.commit()
    flash(f"Slot {slot.slot_number} updated.", "success")
    return redirect(url_for("admin.slots", area_id=slot.area_id))


@admin_bp.post("/slots/<int:slot_id>/delete")
@login_required
@admin_required
def delete_slot(slot_id):
    slot = db.get_or_404(ParkingSlot, slot_id)
    if slot.bookings:
        flash("Slots with booking history cannot be deleted. Mark as MAINTENANCE instead.", "warning")
    else:
        db.session.delete(slot)
        db.session.commit()
        flash("Slot deleted.", "success")
    return redirect(url_for("admin.slots"))


@admin_bp.route("/pricing", methods=["GET", "POST"])
@login_required
@admin_required
def pricing():
    if request.method == "POST":
        name = request.form.get("name", "").strip() or "Standard"
        row = Pricing.query.filter_by(is_active=True).first()
        if not row:
            row = Pricing(name=name)
            db.session.add(row)
        row.name = name
        row.hourly_price = float(request.form.get("hourly_price") or 0)
        row.additional_hour_price = float(request.form.get("additional_hour_price") or 0)
        row.daily_price = float(request.form.get("daily_price") or 0)
        row.grace_period_minutes = int(request.form.get("grace_period_minutes") or 10)
        row.is_active = True
        # Optional override only — default is paid parking fees (no website subscription).
        free_flag = "true" if request.form.get("user_parking_free") else "false"
        set_setting("USER_PARKING_FREE", free_flag)
        db.session.commit()
        flash("Parking fee rates saved. Users pay parking fees only — no website subscription.", "success")
        return redirect(url_for("admin.pricing"))
    return render_template(
        "admin/pricing.html",
        pricing=Pricing.query.filter_by(is_active=True).first(),
        parking_free=is_user_parking_free(),
    )


@admin_bp.route("/payment-policies", methods=["GET", "POST"])
@login_required
@admin_required
def payment_policies():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        amount = float(request.form.get("amount") or 0)
        duration_value = int(request.form.get("duration_value") or 1)
        duration_unit = request.form.get("duration_unit", "MONTH")
        effective_from = request.form.get("effective_from") or date.today().isoformat()
        effective_to = request.form.get("effective_to") or None
        if not name or duration_value < 1 or duration_unit not in ("MONTH", "YEAR"):
            flash("Provide a valid policy name, amount, and duration.", "danger")
        else:
            policy = PaymentPolicy(
                name=name,
                amount=amount,
                duration_value=duration_value,
                duration_unit=duration_unit,
                effective_from=date.fromisoformat(effective_from),
                effective_to=date.fromisoformat(effective_to) if effective_to else None,
                is_active=bool(request.form.get("is_active")),
                free_for_users=bool(request.form.get("free_for_users")),
                notes=request.form.get("notes"),
            )
            # Keep only one active policy if activating
            if policy.is_active:
                PaymentPolicy.query.filter_by(is_active=True).update({"is_active": False})
            db.session.add(policy)
            db.session.commit()
            flash("Parking fee policy saved. It sets how much and for how long rates apply.", "success")
            return redirect(url_for("admin.payment_policies"))
    return render_template(
        "admin/payment_policies.html",
        policies=PaymentPolicy.query.order_by(PaymentPolicy.created_at.desc()).all(),
        parking_free=is_user_parking_free(),
        today=date.today().isoformat(),
    )


@admin_bp.post("/payment-policies/<int:policy_id>/toggle")
@login_required
@admin_required
def toggle_policy(policy_id):
    policy = db.get_or_404(PaymentPolicy, policy_id)
    if not policy.is_active:
        PaymentPolicy.query.filter_by(is_active=True).update({"is_active": False})
        policy.is_active = True
        flash(f"Policy '{policy.name}' is now active for {policy.duration_label}.", "success")
    else:
        policy.is_active = False
        flash(f"Policy '{policy.name}' deactivated.", "info")
    db.session.commit()
    return redirect(url_for("admin.payment_policies"))


@admin_bp.get("/payments")
@login_required
@admin_required
def payments():
    return render_template(
        "admin/payments.html",
        payments=Payment.query.order_by(Payment.created_at.desc()).all(),
        policies=PaymentPolicy.query.order_by(PaymentPolicy.name).all(),
        parking_free=is_user_parking_free(),
    )


@admin_bp.post("/payments/record")
@login_required
@admin_required
def record_payment():
    policy_id = request.form.get("policy_id", type=int)
    amount = float(request.form.get("amount") or 0)
    method = request.form.get("payment_method") or "Cash"
    notes = request.form.get("notes", "").strip()
    policy = db.session.get(PaymentPolicy, policy_id) if policy_id else None
    if policy and amount <= 0:
        amount = policy.amount
    db.session.add(
        Payment(
            transaction_id=f"ADM-{uuid.uuid4().hex[:12].upper()}",
            booking_id=None,
            policy_id=policy.id if policy else None,
            amount=amount,
            payment_method=method,
            status="PAID" if amount > 0 else "WAIVED",
            notes=notes or (f"Admin recorded for policy: {policy.name}" if policy else "Admin recorded payment"),
            recorded_by=current_user.id,
        )
    )
    db.session.commit()
    flash("Payment recorded by admin.", "success")
    return redirect(url_for("admin.payments"))


@admin_bp.get("/reports")
@login_required
@admin_required
def reports():
    by_status = dict(
        db.session.query(Booking.status, func.count(Booking.id)).group_by(Booking.status).all()
    )
    occupancy = {
        "available": ParkingSlot.query.filter_by(status="AVAILABLE").count(),
        "reserved": ParkingSlot.query.filter_by(status="RESERVED").count(),
        "occupied": ParkingSlot.query.filter_by(status="OCCUPIED").count(),
        "maintenance": ParkingSlot.query.filter_by(status="MAINTENANCE").count(),
    }
    revenue = db.session.query(func.coalesce(func.sum(Payment.amount), 0)).scalar() or 0
    monthly = (
        db.session.query(func.strftime("%Y-%m", Booking.created_at), func.count(Booking.id))
        .group_by(func.strftime("%Y-%m", Booking.created_at))
        .order_by(func.strftime("%Y-%m", Booking.created_at).desc())
        .limit(6)
        .all()
    )
    return render_template(
        "admin/reports.html",
        by_status=by_status,
        occupancy=occupancy,
        revenue=revenue,
        monthly=list(reversed(monthly)),
        total_bookings=Booking.query.count(),
        total_users=User.query.filter_by(role="USER").count(),
        parking_free=is_user_parking_free(),
    )


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
        notify(
            booking.user_id,
            "Checked in",
            f"Vehicle checked in for {booking.booking_id}.",
            "BOOKING",
            link=url_for("booking.detail", booking_id=booking.id),
            email=booking.user.email,
        )
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
        fee = 0.0 if is_user_parking_free() else (booking.estimated_fee or 0)
        booking.final_fee = fee
        booking.slot.status = "AVAILABLE"
        db.session.add(
            Payment(
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
                booking_id=booking.id,
                amount=fee,
                payment_method="Cash" if fee > 0 else "FREE",
                status="PAID" if fee > 0 else "WAIVED",
                notes="Parking fee collected at checkout." if fee > 0 else "Parking fee waived by admin setting.",
                recorded_by=current_user.id,
            )
        )
        notify(
            booking.user_id,
            "Checkout complete",
            f"Parking session {booking.booking_id} completed. Amount: INR {fee:.2f}.",
            "PAYMENT",
            link=url_for("booking.detail", booking_id=booking.id),
            email=booking.user.email,
        )
        db.session.commit()
        flash(f"Vehicle checked out. Parking fee: INR {fee:.2f}.", "success")
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
