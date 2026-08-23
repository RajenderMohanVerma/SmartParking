from app import create_app, db

app = create_app()


@app.route("/init-db")
def init_db():
    """One-time route to create all DB tables on Vercel. Remove after first use."""
    try:
        db.create_all()
        return "<h2>✅ Database tables created successfully!</h2><p>Now remove this route and redeploy.</p>", 200
    except Exception as e:
        return f"<h2>❌ Error: {e}</h2>", 500


if __name__ == "__main__":
    app.run(debug=True)
