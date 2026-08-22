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
    if not ParkingArea.query.first():
        for name, location, prefix in [("Central Plaza", "Connaught Place", "A"), ("Riverside Deck", "Pragati Maidan", "B")]:
            area = ParkingArea(name=name, location=location, description="Managed SmartPark facility", floors=2)
            db.session.add(area)
            db.session.flush()
            for number in range(1, 9):
                db.session.add(ParkingSlot(area_id=area.id, slot_number=f"{prefix}{number:02d}", slot_type="EV" if number == 8 else "Normal", price=45 if number == 8 else 30))
    if not Pricing.query.first():
        db.session.add(Pricing(name="Standard hourly", hourly_price=30, additional_hour_price=20, daily_price=250, grace_period_minutes=10))
    db.session.commit()
    print("SmartPark demo data is ready.")
