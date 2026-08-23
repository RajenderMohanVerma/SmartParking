from app import create_app, db

app = create_app()


@app.route("/admin/seed-demo")
def seed_demo():
    """
    Admin-only route to insert demo parking areas + slots.
    Only works when logged in as ADMIN.
    Safe to call multiple times — skips existing data.
    """
    from flask_login import current_user
    if not current_user.is_authenticated or current_user.role != "ADMIN":
        return "<h2>403 — Admins only.</h2>", 403

    from app.models import ParkingArea, ParkingSlot

    demo_areas = [
        {
            "name": "Central Parking Block A",
            "location": "Connaught Place, New Delhi 110001",
            "operating_hours": "Open 24 hours",
            "description": "Multi-level parking at the heart of the city. Covered, CCTV monitored.",
            "floors": 3,
            "slots": [
                {"prefix": "A", "start": 1, "count": 12, "floor": 1, "type": "Normal",    "vehicle": "Any",  "price": 30},
                {"prefix": "B", "start": 1, "count": 8,  "floor": 2, "type": "Premium",   "vehicle": "Car",  "price": 50},
                {"prefix": "C", "start": 1, "count": 4,  "floor": 3, "type": "EV Charging","vehicle": "EV",  "price": 40},
            ],
        },
        {
            "name": "South Delhi Parking Hub",
            "location": "Saket District Centre, New Delhi 110017",
            "operating_hours": "06:00 – 23:00",
            "description": "Near Select CITYWALK mall. Bike and car slots available.",
            "floors": 2,
            "slots": [
                {"prefix": "A", "start": 1, "count": 10, "floor": 1, "type": "Normal",  "vehicle": "Car",  "price": 25},
                {"prefix": "B", "start": 1, "count": 6,  "floor": 1, "type": "Compact", "vehicle": "Bike", "price": 15},
                {"prefix": "C", "start": 1, "count": 4,  "floor": 2, "type": "SUV",     "vehicle": "SUV",  "price": 60},
            ],
        },
        {
            "name": "East Delhi Transit Park",
            "location": "Anand Vihar ISBT, Delhi 110092",
            "operating_hours": "Open 24 hours",
            "description": "Long-stay and transit parking near metro and bus terminal.",
            "floors": 1,
            "slots": [
                {"prefix": "P", "start": 1, "count": 20, "floor": 1, "type": "Normal",     "vehicle": "Any",  "price": 20},
                {"prefix": "H", "start": 1, "count": 2,  "floor": 1, "type": "Handicapped","vehicle": "Any",  "price": 10},
            ],
        },
    ]

    created_areas = 0
    created_slots = 0
    skipped = 0

    for ad in demo_areas:
        area = ParkingArea.query.filter_by(name=ad["name"]).first()
        if not area:
            area = ParkingArea(
                name=ad["name"],
                location=ad["location"],
                operating_hours=ad["operating_hours"],
                description=ad["description"],
                floors=ad["floors"],
                status="ACTIVE",
            )
            db.session.add(area)
            db.session.flush()   # get area.id before commit
            created_areas += 1

        for sg in ad["slots"]:
            for i in range(sg["start"], sg["start"] + sg["count"]):
                snum = f"{sg['prefix']}{i:02d}"
                exists = ParkingSlot.query.filter_by(area_id=area.id, slot_number=snum).first()
                if exists:
                    skipped += 1
                    continue
                db.session.add(ParkingSlot(
                    area_id=area.id,
                    slot_number=snum,
                    floor=sg["floor"],
                    slot_type=sg["type"],
                    vehicle_type=sg["vehicle"],
                    price=sg["price"],
                    status="AVAILABLE",
                ))
                created_slots += 1

    db.session.commit()

    return f"""
    <html><body style='font-family:sans-serif;padding:40px;max-width:600px;'>
    <h2>✅ Demo data seeded!</h2>
    <ul>
      <li><b>Areas created:</b> {created_areas}</li>
      <li><b>Slots created:</b> {created_slots}</li>
      <li><b>Skipped (already exist):</b> {skipped}</li>
    </ul>
    <h3>What was added:</h3>
    <ul>
      <li>Central Parking Block A — 24 slots (Normal, Premium, EV)</li>
      <li>South Delhi Parking Hub — 20 slots (Car, Bike, SUV)</li>
      <li>East Delhi Transit Park — 22 slots (Normal, Handicapped)</li>
    </ul>
    <p><a href="/admin/areas" style="color:#087f8c;font-weight:700;">→ Go to Admin Areas</a></p>
    <p><a href="/parking" style="color:#087f8c;font-weight:700;">→ View Live Parking Page</a></p>
    </body></html>
    """, 200


if __name__ == "__main__":
    app.run(debug=True)
