from datetime import datetime, timedelta

from app import create_app, db
from app.models import ParkingArea, ParkingSlot, Pricing, SystemSetting, User, Vehicle


def make_app():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(SystemSetting(key="USER_PARKING_FREE", value="false"))
        user = User(full_name="Test User", username="tester", email="tester@example.com")
        user.set_password("Password1")
        db.session.add(user)
        area = ParkingArea(name="Test Area", location="Test City")
        db.session.add(area)
        db.session.flush()
        db.session.add(ParkingSlot(area_id=area.id, slot_number="A01", price=30))
        db.session.add(Pricing(name="Default", hourly_price=30, additional_hour_price=20))
        db.session.commit()
    return app


def test_register_login_and_book():
    app = make_app()
    client = app.test_client()
    response = client.post("/auth/login", data={"email": "tester@example.com", "password": "Password1"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="tester@example.com").first()
        vehicle = Vehicle(user_id=user.id, vehicle_number="TEST123", vehicle_type="Car")
        db.session.add(vehicle)
        db.session.commit()
        slot = ParkingSlot.query.first()
        slot_id, vehicle_id = slot.id, vehicle.id
    entry = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=1)
    exit_time = entry + timedelta(hours=2)
    response = client.post(
        "/bookings/new",
        data={
            "slot_id": slot_id,
            "vehicle_id": vehicle_id,
            "entry_time": entry.isoformat(timespec="minutes"),
            "expected_exit_time": exit_time.isoformat(timespec="minutes"),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        slot = ParkingSlot.query.first()
        assert slot.status == "RESERVED"
        from app.models import Booking

        booking = Booking.query.first()
        assert booking is not None
        assert booking.estimated_fee > 0


def test_roles_page_and_admin_pricing():
    app = make_app()
    client = app.test_client()
    assert client.get("/roles").status_code == 200
    with app.app_context():
        admin = User(full_name="Admin", username="admin", email="admin@example.com", role="ADMIN")
        admin.set_password("Admin@123")
        db.session.add(admin)
        db.session.commit()
    client.post("/auth/login", data={"email": "admin@example.com", "password": "Admin@123"}, follow_redirects=True)
    assert client.get("/admin/pricing").status_code == 200
    assert client.get("/admin/payment-policies").status_code == 200
    assert client.get("/admin/slots").status_code == 200
    assert client.get("/admin/reports").status_code == 200
