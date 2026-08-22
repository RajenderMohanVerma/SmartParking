import math


def calculate_fee(start, end, pricing, grace_minutes=10):
    minutes = max(1, math.ceil((end - start).total_seconds() / 60))
    hours = math.ceil(minutes / 60)
    if hours <= 1:
        base = pricing.hourly_price
        additional = 0
    else:
        base = pricing.hourly_price
        additional = (hours - 1) * pricing.additional_hour_price
    return round(base + additional, 2)
