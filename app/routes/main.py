from flask import Blueprint, current_app, render_template, send_from_directory
from app.models import ParkingArea, ParkingSlot

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("home.html", areas=ParkingArea.query.filter_by(status="ACTIVE").all(), slot_count=ParkingSlot.query.count())


@main_bp.get("/health")
def health():
    return {"status": "ok"}


@main_bp.get("/sw.js")
def service_worker():
    return send_from_directory(current_app.static_folder, "sw.js", mimetype="application/javascript")
