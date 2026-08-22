from app import create_app, db
from app.models import ParkingArea, ParkingSlot, Pricing, User, Vehicle


def make_app():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    with app.app_context():
        db.drop_all(); db.create_all()
        user = User(full_name="Test User", username="tester", email="tester@example.com")
        user.set_password("Password1")
        db.session.add(user)
        area = ParkingArea(name="Test Area", location="Test City")
        db.session.add(area); db.session.flush()
        db.session.add(ParkingSlot(area_id=area.id, slot_number="A01", price=30))
        db.session.add(Pricing(name="Default", hourly_price=30, additional_hour_price=20))
        db.session.commit()
    return app


def test_register_login_and_book():
    app = make_app(); client = app.test_client()
    response = client.post("/auth/login", data={"email":"tester@example.com", "password":"Password1"}, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction():
        pass
    with app.app_context():
        user = User.query.filter_by(email="tester@example.com").first()
        vehicle = Vehicle(user_id=user.id, vehicle_number="TEST123", vehicle_type="Car")
        db.session.add(vehicle); db.session.commit()
        slot = ParkingSlot.query.first()
        slot_id, vehicle_id = slot.id, vehicle.id
    from datetime import datetime, timedelta
    entry = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=1)
    exit_time = entry + timedelta(hours=2)
    response = client.post("/bookings/new", data={"slot_id":slot_id,"vehicle_id":vehicle_id,"entry_time":entry.isoformat(timespec="minutes"),"expected_exit_time":exit_time.isoformat(timespec="minutes")}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert ParkingSlot.query.first().status == "RESERVED"
