from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy import or_

from app.models import ParkingArea, ParkingSlot

parking_bp = Blueprint("parking", __name__)


@parking_bp.get("")
@login_required
def index():
    query = ParkingSlot.query.join(ParkingArea).filter(ParkingArea.status == "ACTIVE")
    search = request.args.get("q", "").strip()
    slot_type = request.args.get("slot_type", "")
    if search:
        query = query.filter(or_(ParkingArea.name.ilike(f"%{search}%"), ParkingArea.location.ilike(f"%{search}%"), ParkingSlot.slot_number.ilike(f"%{search}%")))
    if slot_type:
        query = query.filter(ParkingSlot.slot_type == slot_type)
    return render_template("parking/index.html", slots=query.order_by(ParkingArea.name, ParkingSlot.slot_number).all())


@parking_bp.get("/api/slots")
def slots_api():
    return jsonify([{"id": slot.id, "number": slot.slot_number, "area": slot.area.name, "status": slot.status, "type": slot.slot_type} for slot in ParkingSlot.query.all()])
