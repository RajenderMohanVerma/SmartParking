from datetime import datetime, timezone
import secrets

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


def utcnow():
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class User(UserMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="USER", nullable=False)
    profile_photo = db.Column(db.String(255))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    vehicles = db.relationship("Vehicle", back_populates="user", cascade="all, delete-orphan")
    bookings = db.relationship("Booking", back_populates="user")
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Vehicle(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    vehicle_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    vehicle_type = db.Column(db.String(30), nullable=False)
    brand = db.Column(db.String(60))
    model = db.Column(db.String(60))
    color = db.Column(db.String(30))
    fuel_type = db.Column(db.String(30))
    notes = db.Column(db.Text)
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship("User", back_populates="vehicles")
    bookings = db.relationship("Booking", back_populates="vehicle")


class ParkingArea(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    floors = db.Column(db.Integer, default=1)
    operating_hours = db.Column(db.String(80), default="Open 24 hours")
    status = db.Column(db.String(20), default="ACTIVE", nullable=False)
    slots = db.relationship("ParkingSlot", back_populates="area", cascade="all, delete-orphan")
    bookings = db.relationship("Booking", back_populates="area")


class ParkingSlot(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey("parking_area.id"), nullable=False)
    slot_number = db.Column(db.String(20), nullable=False)
    floor = db.Column(db.Integer, default=1)
    slot_type = db.Column(db.String(30), default="Normal")
    vehicle_type = db.Column(db.String(30), default="Any")
    price = db.Column(db.Float, default=30)
    status = db.Column(db.String(20), default="AVAILABLE", nullable=False, index=True)
    location_info = db.Column(db.String(120))
    area = db.relationship("ParkingArea", back_populates="slots")
    bookings = db.relationship("Booking", back_populates="slot")
    __table_args__ = (db.UniqueConstraint("area_id", "slot_number", name="uq_area_slot"),)


class Booking(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(30), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    parking_area_id = db.Column(db.Integer, db.ForeignKey("parking_area.id"), nullable=False)
    parking_slot_id = db.Column(db.Integer, db.ForeignKey("parking_slot.id"), nullable=False)
    booking_date = db.Column(db.Date, nullable=False, index=True)
    entry_time = db.Column(db.DateTime(timezone=True), nullable=False)
    expected_exit_time = db.Column(db.DateTime(timezone=True), nullable=False)
    actual_entry_time = db.Column(db.DateTime(timezone=True))
    actual_exit_time = db.Column(db.DateTime(timezone=True))
    estimated_fee = db.Column(db.Float, default=0)
    final_fee = db.Column(db.Float)
    status = db.Column(db.String(20), default="CONFIRMED", nullable=False, index=True)
    qr_token = db.Column(db.String(64), unique=True, default=lambda: secrets.token_urlsafe(32), nullable=False)
    user = db.relationship("User", back_populates="bookings")
    vehicle = db.relationship("Vehicle", back_populates="bookings")
    area = db.relationship("ParkingArea", back_populates="bookings")
    slot = db.relationship("ParkingSlot", back_populates="bookings")
    payment = db.relationship("Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan")


class Payment(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(40), unique=True, nullable=False, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=True)
    policy_id = db.Column(db.Integer, db.ForeignKey("payment_policy.id"), nullable=True)
    amount = db.Column(db.Float, nullable=False, default=0)
    payment_method = db.Column(db.String(30), default="Cash")
    status = db.Column(db.String(20), default="PAID")
    notes = db.Column(db.Text)
    paid_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    recorded_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    booking = db.relationship("Booking", back_populates="payment")
    policy = db.relationship("PaymentPolicy", back_populates="payments")


class Pricing(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    vehicle_type = db.Column(db.String(30), default="Any")
    slot_type = db.Column(db.String(30), default="Any")
    hourly_price = db.Column(db.Float, default=30)
    additional_hour_price = db.Column(db.Float, default=20)
    daily_price = db.Column(db.Float, default=250)
    grace_period_minutes = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)


class PaymentPolicy(TimestampMixin, db.Model):
    """Admin parking-fee rate card: amount and how long (months/years) it stays in force.
    This is NOT a website subscription — users only pay parking fees.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=30)
    duration_value = db.Column(db.Integer, nullable=False, default=1)
    duration_unit = db.Column(db.String(10), nullable=False, default="MONTH")  # MONTH | YEAR
    effective_from = db.Column(db.Date, nullable=False)
    effective_to = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    free_for_users = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.Column(db.Text)
    payments = db.relationship("Payment", back_populates="policy")

    @property
    def duration_label(self):
        unit = "month" if self.duration_unit == "MONTH" else "year"
        if self.duration_value != 1:
            unit += "s"
        return f"{self.duration_value} {unit}"


class Notification(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(30), default="INFO")
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    link = db.Column(db.String(255))
    user = db.relationship("User", back_populates="notifications")


class PasswordResetToken(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    used = db.Column(db.Boolean, default=False)


class SystemSetting(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)


class ActivityLog(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    action = db.Column(db.String(80), nullable=False, index=True)
    target_type = db.Column(db.String(40))
    target_id = db.Column(db.String(80))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user = db.relationship("User")


class FavoriteArea(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    area_id = db.Column(db.Integer, db.ForeignKey("parking_area.id"), nullable=False, index=True)
    user = db.relationship("User", backref=db.backref("favorite_areas", cascade="all, delete-orphan"))
    area = db.relationship("ParkingArea")
    __table_args__ = (db.UniqueConstraint("user_id", "area_id", name="uq_user_favorite_area"),)

