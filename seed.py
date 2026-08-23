from datetime import date

from app import create_app, db
from app.models import ParkingArea, ParkingSlot, PaymentPolicy, Pricing, SystemSetting, User, Vehicle

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
        db.session.add(Vehicle(user_id=user.id, vehicle_number="DL01AB1234", vehicle_type="Car", brand="Honda", model="City", is_default=False))
    Vehicle.query.update({"is_default": False})
    parking_locations = [
        ("Central Plaza", "Connaught Place, New Delhi 110001", "A"),
        ("Riverside Deck", "Pragati Maidan, New Delhi 110001", "B"),
        ("Palika Parking, Connaught Place", "Baba Kharak Singh Marg, Near Connaught Place, New Delhi 110001", "CP"),
        ("MCD Multi-Level Parking, Sarojini Nagar", "Sarojini Nagar Market, Near Sarojini Nagar Metro Station, New Delhi 110023", "SN"),
        ("DDA Parking, INA Market", "Sri Aurobindo Marg, INA Market, New Delhi 110023", "INA"),
        ("MCD Parking, Karol Bagh", "Ajmal Khan Road, Near Karol Bagh Metro Station, New Delhi 110005", "KB"),
        ("MCD Parking, Chandni Chowk", "Near Fatehpuri Masjid, Chandni Chowk, Delhi 110006", "CC"),
        ("DDA Parking, Nehru Place", "Nehru Place District Centre, New Delhi 110019", "NP"),
        ("DDA Parking, Anand Vihar", "Near Anand Vihar ISBT, Delhi 110092", "AV"),
        ("New Delhi Railway Station Parking", "Ajmeri Gate side, New Delhi Railway Station, New Delhi 110002", "NRS"),
        ("Select CITYWALK Parking", "District Centre, Saket, Press Enclave Marg, New Delhi 110017", "SW"),
        ("DLF Promenade Parking", "Nelson Mandela Road, Vasant Kunj, New Delhi 110070", "DP"),
        ("Ambience Mall Parking", "Nelson Mandela Road, Vasant Kunj, New Delhi 110070", "AM"),
        ("India Habitat Centre Parking", "Lodhi Road, New Delhi 110003", "IHC"),
        ("DLF Avenue Saket Parking", "District Centre, Saket, New Delhi 110017", "DA"),
        ("Pacific Mall Tagore Garden Parking", "Najafgarh Road, Tagore Garden, New Delhi 110027", "PT"),
        ("IGI Airport Parking, Terminal 3", "Indira Gandhi International Airport, Terminal 3, New Delhi 110037", "IGI"),
    ]
    for name, location, prefix in parking_locations:
        area = ParkingArea.query.filter_by(name=name).first()
        if not area:
            area = ParkingArea(name=name, location=location, description="SmartPark Delhi directory facility", floors=2)
            db.session.add(area)
            db.session.flush()
        elif area.location != location:
            area.location = location
        if not area.slots:
            for number in range(1, 9):
                db.session.add(
                    ParkingSlot(
                        area_id=area.id,
                        slot_number=f"{prefix}{number:02d}",
                        slot_type="EV" if number == 8 else "Normal",
                        price=45 if number == 8 else 30,
                    )
                )
            db.session.flush()
        existing_slots = ParkingSlot.query.filter_by(area_id=area.id).all()
        existing_types = {slot.slot_type for slot in existing_slots}
        extra_types = [("VIP", 60), ("Accessible", 30), ("Compact", 25), ("Motorcycle", 15)]
        for slot_type, price in extra_types:
            if slot_type not in existing_types:
                slot_number = f"{prefix}-{slot_type[:3].upper()}"
                if not ParkingSlot.query.filter_by(area_id=area.id, slot_number=slot_number).first():
                    db.session.add(ParkingSlot(area_id=area.id, slot_number=slot_number, slot_type=slot_type, price=price))
    if not Pricing.query.first():
        db.session.add(Pricing(name="Standard hourly", hourly_price=30, additional_hour_price=20, daily_price=250, grace_period_minutes=10))
    if not SystemSetting.query.filter_by(key="USER_PARKING_FREE").first():
        db.session.add(SystemSetting(key="USER_PARKING_FREE", value="false"))
    if not PaymentPolicy.query.first():
        today = date.today()
        db.session.add(
            PaymentPolicy(
                name="Standard 2026 parking fees",
                amount=30,
                duration_value=1,
                duration_unit="YEAR",
                effective_from=today,
                effective_to=date(today.year + 1, today.month, today.day),
                is_active=True,
                free_for_users=False,
                notes="Users pay parking session fees only — no website subscription.",
            )
        )
    db.session.commit()
    print("SmartPark demo data is ready.")
