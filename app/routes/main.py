from flask import Blueprint, current_app, render_template, send_from_directory
from sqlalchemy import func

from app import db
from app.models import Booking, ParkingArea, ParkingSlot, Payment

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    slot_status = dict(
        db.session.query(ParkingSlot.status, func.count(ParkingSlot.id))
        .group_by(ParkingSlot.status)
        .all()
    )
    return render_template(
        "home.html",
        areas=ParkingArea.query.filter_by(status="ACTIVE").all(),
        slot_count=ParkingSlot.query.count(),
        live_slots=(
            ParkingSlot.query.join(ParkingArea)
            .filter(ParkingArea.status == "ACTIVE")
            .order_by(ParkingArea.name, ParkingSlot.slot_number)
            .limit(12)
            .all()
        ),
        slot_status=slot_status,
        available_count=slot_status.get("AVAILABLE", 0),
        reserved_count=slot_status.get("RESERVED", 0),
        occupied_count=slot_status.get("OCCUPIED", 0),
        maintenance_count=slot_status.get("MAINTENANCE", 0),
        booking_count=Booking.query.count(),
        payment_count=Payment.query.filter_by(status="PAID").count(),
    )


@main_bp.get("/roles")
def roles():
    return render_template("roles.html")


@main_bp.get("/health")
def health():
    return {"status": "ok"}


@main_bp.get("/sw.js")
def service_worker():
    return send_from_directory(current_app.static_folder, "sw.js", mimetype="application/javascript")
