from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy import or_

from app.models import ParkingArea, ParkingSlot

parking_bp = Blueprint("parking", __name__)

DELHI_DIRECTORY = [
    {"name": "Palika Parking, Connaught Place", "area": "Central Delhi", "address": "Baba Kharak Singh Marg, Near Connaught Place, New Delhi 110001", "type": "Government", "operator": "NDMC", "hours": "24 hours", "note": "Central business district parking directory listing."},
    {"name": "MCD Multi-Level Parking, Sarojini Nagar", "area": "South Delhi", "address": "Sarojini Nagar Market, Near Sarojini Nagar Metro Station, New Delhi 110023", "type": "Government", "operator": "MCD", "hours": "06:00 - 23:00", "note": "Market parking; verify entry availability on arrival."},
    {"name": "DDA Parking, INA Market", "area": "South Delhi", "address": "Sri Aurobindo Marg, INA Market, New Delhi 110023", "type": "Government", "operator": "DDA", "hours": "06:00 - 22:00", "note": "Public parking near INA Market and metro access."},
    {"name": "MCD Parking, Karol Bagh", "area": "West Delhi", "address": "Ajmal Khan Road, Near Karol Bagh Metro Station, New Delhi 110005", "type": "Government", "operator": "MCD", "hours": "07:00 - 22:00", "note": "Market-area parking directory listing."},
    {"name": "MCD Parking, Chandni Chowk", "area": "Old Delhi", "address": "Near Fatehpuri Masjid, Chandni Chowk, Delhi 110006", "type": "Government", "operator": "MCD", "hours": "07:00 - 22:00", "note": "Useful for Chandni Chowk and Red Fort visitors."},
    {"name": "DDA Parking, Nehru Place", "area": "South East Delhi", "address": "Nehru Place District Centre, Near Nehru Place Metro Station, New Delhi 110019", "type": "Government", "operator": "DDA", "hours": "06:00 - 23:00", "note": "Business district parking near the metro interchange."},
    {"name": "DDA Parking, Anand Vihar", "area": "East Delhi", "address": "Near Anand Vihar ISBT and Anand Vihar Metro Station, Delhi 110092", "type": "Government", "operator": "DDA", "hours": "24 hours", "note": "Transit parking near ISBT and railway access."},
    {"name": "New Delhi Railway Station Parking", "area": "Central Delhi", "address": "Ajmeri Gate side, New Delhi Railway Station, New Delhi 110002", "type": "Government", "operator": "Indian Railways", "hours": "24 hours", "note": "Station access parking; follow railway security directions."},
    {"name": "IGI Airport Parking, Terminal 3", "area": "South West Delhi", "address": "Indira Gandhi International Airport, Terminal 3, New Delhi 110037", "type": "Private", "operator": "Delhi International Airport", "hours": "24 hours", "note": "Airport parking; terminal access and tariffs vary by zone."},
    {"name": "DLF Promenade Parking", "area": "Vasant Kunj", "address": "Nelson Mandela Road, Vasant Kunj, New Delhi 110070", "type": "Private", "operator": "DLF", "hours": "10:00 - 23:00", "note": "Mall parking with EV facilities subject to availability."},
    {"name": "Ambience Mall Parking", "area": "Vasant Kunj", "address": "Nelson Mandela Road, Vasant Kunj, New Delhi 110070", "type": "Private", "operator": "Ambience Mall", "hours": "10:00 - 23:00", "note": "Large private facility; verify current rates at entry."},
    {"name": "India Habitat Centre Parking", "area": "Lodhi Road", "address": "Lodhi Road, Near India Habitat Centre, New Delhi 110003", "type": "Private", "operator": "India Habitat Centre", "hours": "08:00 - 22:00", "note": "Visitor parking subject to venue access rules."},
    {"name": "DLF Avenue Saket Parking", "area": "Saket", "address": "District Centre, Saket, New Delhi 110017", "type": "Private", "operator": "DLF Avenue", "hours": "10:00 - 23:00", "note": "Retail and dining destination parking."},
    {"name": "Pacific Mall Tagore Garden Parking", "area": "West Delhi", "address": "Najafgarh Road, Tagore Garden, New Delhi 110027", "type": "Private", "operator": "Pacific Mall", "hours": "10:00 - 22:00", "note": "Mall parking near Tagore Garden metro access."},
    {"name": "Select CITYWALK Parking", "area": "Saket", "address": "District Centre, Saket, Press Enclave Marg, New Delhi 110017", "type": "Private", "operator": "Select CITYWALK", "hours": "10:00 - 23:00", "note": "Shopping destination parking; charges and capacity vary."},
]


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
    directory_type = request.args.get("directory_type", "All")
    directory_search = request.args.get("directory_q", "").strip().lower()
    directory = []
    for place in DELHI_DIRECTORY:
        if directory_type not in ("All", "") and place["type"] != directory_type:
            continue
        if directory_search and not any(directory_search in place[key].lower() for key in ("name", "area", "operator")):
            continue
        parking_area = ParkingArea.query.filter_by(name=place["name"]).first()
        place = {**place, "parking_area": parking_area}
        if parking_area:
            place["total_spaces"] = len(parking_area.slots)
            place["available_spaces"] = sum(slot.status == "AVAILABLE" for slot in parking_area.slots)
            place["occupied_spaces"] = sum(slot.status == "OCCUPIED" for slot in parking_area.slots)
        else:
            place["total_spaces"] = place["available_spaces"] = place["occupied_spaces"] = 0
        directory.append(place)
    return render_template("parking/index.html", slots=query.order_by(ParkingArea.name, ParkingSlot.slot_number).all(), directory=directory, directory_total=len(DELHI_DIRECTORY))


@parking_bp.get("/api/slots")
def slots_api():
    return jsonify([{"id": slot.id, "number": slot.slot_number, "area": slot.area.name, "status": slot.status, "type": slot.slot_type} for slot in ParkingSlot.query.all()])


@parking_bp.get("/api/directory")
def directory_api():
    return jsonify([{"name": area.name, "total": len(area.slots), "available": sum(slot.status == "AVAILABLE" for slot in area.slots), "next_slot_id": next((slot.id for slot in area.slots if slot.status == "AVAILABLE"), None)} for area in ParkingArea.query.filter_by(status="ACTIVE").all()])
