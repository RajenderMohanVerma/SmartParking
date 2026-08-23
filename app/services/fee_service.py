import math
from datetime import date

from app.models import PaymentPolicy, SystemSetting


def is_user_parking_free():
    """Website has no subscription. Parking fees apply unless admin turns fees off."""
    setting = SystemSetting.query.filter_by(key="USER_PARKING_FREE").first()
    if setting:
        return setting.value.lower() in ("1", "true", "yes", "on")
    return False


def active_payment_policy():
    today = date.today()
    policies = PaymentPolicy.query.filter_by(is_active=True).order_by(PaymentPolicy.effective_from.desc()).all()
    for policy in policies:
        if policy.effective_from and policy.effective_from > today:
            continue
        if policy.effective_to and policy.effective_to < today:
            continue
        return policy
    return None


def calculate_fee(start, end, pricing, grace_minutes=10):
    if is_user_parking_free():
        return 0.0
    policy = active_payment_policy()
    hourly = pricing.hourly_price if pricing else 30
    additional = pricing.additional_hour_price if pricing else 20
    # Active admin policy can override base hourly amount while it is in force.
    if policy and not policy.free_for_users and policy.amount > 0:
        hourly = policy.amount
        additional = policy.amount if additional <= 0 else additional
    minutes = max(1, math.ceil((end - start).total_seconds() / 60))
    hours = math.ceil(minutes / 60)
    if hours <= 1:
        return round(hourly, 2)
    return round(hourly + (hours - 1) * additional, 2)


def get_setting(key, default=""):
    row = SystemSetting.query.filter_by(key=key).first()
    return row.value if row else default


def set_setting(key, value):
    from app import db

    row = SystemSetting.query.filter_by(key=key).first()
    if row:
        row.value = str(value)
    else:
        db.session.add(SystemSetting(key=key, value=str(value)))
