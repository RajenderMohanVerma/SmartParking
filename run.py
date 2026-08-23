from app import create_app, db

app = create_app()


@app.route("/init-db")
def init_db():
    """One-time route to create all DB tables + seed admin on Vercel."""
    try:
        db.create_all()

        # Seed admin user if not exists
        from app.models import User
        if not User.query.filter_by(email="admin@smartpark.com").first():
            admin = User(
                full_name="SmartPark Admin",
                username="admin",
                email="admin@smartpark.com",
                role="ADMIN",
                email_verified=True,
            )
            admin.set_password("Admin@123")
            db.session.add(admin)
            db.session.commit()
            seeded = "Admin user created: admin@smartpark.com / Admin@123"
        else:
            seeded = "Admin user already exists."

        return f"""
        <html><body style='font-family:sans-serif;padding:40px;'>
        <h2>✅ Database initialized!</h2>
        <p><b>Tables:</b> All created successfully.</p>
        <p><b>Seed:</b> {seeded}</p>
        <hr>
        <p style='color:red;'><b>⚠️ IMPORTANT:</b> Remove this /init-db route now and redeploy for security!</p>
        </body></html>
        """, 200
    except Exception as e:
        return f"<html><body style='font-family:sans-serif;padding:40px;'><h2>❌ Error</h2><pre>{e}</pre></body></html>", 500


if __name__ == "__main__":
    app.run(debug=True)
