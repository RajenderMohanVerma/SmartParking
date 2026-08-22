from datetime import datetime, timedelta, timezone

from app import create_app, db
from app.models import ParkingArea, ParkingSlot, Pricing, User, Vehicle

app = create_app()

with app.app_context():
    if not User.query.filter_by(email="admin@smartpark.com").first():
        admin = User(full_name="SmartPark Admin", username="admin", email="admin@smartpark.com", role="ADMIN", email_verified=True)
        admin.set_password("Admin@123")
        db.session.add(admin)
    if not User.query.filter_by(email="user@smartpark.com").first():
        user = User(full_name="Demo Driver", username="demo", email="user@smartpark.com", phone="9876543210", email_verified=True)
        user.set_password("User@123")
        db.session.add(user)
        db.session.flush()
        db.session.add(Vehicle(user_id=user.id, vehicle_number="DL01AB1234", vehicle_type="Car", brand="Honda", model="City", is_default=True))
    parking_locations = [("Central Plaza", "Connaught Place", "A"), ("Riverside Deck", "Pragati Maidan", "B"), ("Palika Parking, Connaught Place", "Central Delhi", "CP"), ("MCD Multi-Level Parking, Sarojini Nagar", "South Delhi", "SN"), ("DDA Parking, INA Market", "South Delhi", "INA"), ("MCD Parking, Karol Bagh", "West Delhi", "KB"), ("Select CITYWALK Parking", "Saket", "SW"), ("DLF Promenade Parking", "Vasant Kunj", "DP"), ("Ambience Mall Parking", "Vasant Kunj", "AM"), ("India Habitat Centre Parking", "Lodhi Road", "IHC")]
    for name, location, prefix in parking_locations:
        area = ParkingArea.query.filter_by(name=name).first()
        if not area:
            area = ParkingArea(name=name, location=location, description="SmartPark Delhi directory facility", floors=2)
            db.session.add(area)
            db.session.flush()
        if not area.slots:
            for number in range(1, 9):
                db.session.add(ParkingSlot(area_id=area.id, slot_number=f"{prefix}{number:02d}", slot_type="EV" if number == 8 else "Normal", price=45 if number == 8 else 30))
            db.session.flush()
        existing_types = {slot.slot_type for slot in area.slots}
        extra_types = [("VIP", 60), ("Accessible", 30), ("Compact", 25), ("Motorcycle", 15)]
        next_number = len(area.slots) + 1
        for slot_type, price in extra_types:
            if slot_type not in existing_types:
                db.session.add(ParkingSlot(area_id=area.id, slot_number=f"{prefix}{next_number:02d}", slot_type=slot_type, price=price))
                next_number += 1
    if not Pricing.query.first():
        db.session.add(Pricing(name="Standard hourly", hourly_price=30, additional_hour_price=20, daily_price=250, grace_period_minutes=10))
    db.session.commit()
    print("SmartPark demo data is ready.")
