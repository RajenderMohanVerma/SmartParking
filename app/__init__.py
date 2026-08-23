from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    if isinstance(config_class, dict):
        app.config.from_object(Config)
        app.config.update(config_class)
    else:
        app.config.from_object(config_class)

    # Only create directories locally — Vercel filesystem is read-only
    import os
    if not os.getenv("VERCEL"):
        try:
            Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
            Path(app.instance_path).mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to continue."
    mail.init_app(app)
    csrf.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.user import user_bp
    from app.routes.parking import parking_bp
    from app.routes.booking import booking_bp
    from app.routes.admin import admin_bp
    from app.routes.payment import payment_bp
    from app.routes.notification import notification_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(parking_bp, url_prefix="/parking")
    app.register_blueprint(booking_bp, url_prefix="/bookings")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(payment_bp, url_prefix="/payments")
    app.register_blueprint(notification_bp, url_prefix="/notifications")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    @app.context_processor
    def inject_globals():
        from app.models import Notification
        unread = 0
        if not app.config.get("LOGIN_DISABLED", False):
            from flask_login import current_user
            if current_user.is_authenticated:
                unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        return {"unread_notifications": unread}

    with app.app_context():
        # Only auto-create tables locally; on Vercel use /init-db route
        import os
        if not os.getenv("VERCEL"):
            db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return db.session.get(User, int(user_id))
