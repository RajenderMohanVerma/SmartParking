from datetime import datetime, timedelta, timezone
import secrets
from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_

from app import db
from app.models import PasswordResetToken, User
from app.services.email_service import send_email

auth_bp = Blueprint("auth", __name__)


def safe_next_url(target):
    if not target:
        return None
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    if redirect_url.scheme in ("http", "https") and redirect_url.netloc == host_url.netloc:
        return redirect_url.path
    return None


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user.dashboard"))
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not full_name or not username or not email or len(password) < 8 or password != request.form.get("confirm_password", ""):
            flash("Complete every field, use 8+ characters, and make passwords match.", "danger")
        elif User.query.filter(or_(User.email == email, User.username == username)).first():
            flash("That email or username is already registered.", "danger")
        else:
            user = User(full_name=full_name, username=username, email=email, phone=request.form.get("phone"))
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. You can sign in now.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and user.is_active and user.check_password(request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(safe_next_url(request.args.get("next")) or url_for("user.dashboard"))
        flash("Invalid credentials or inactive account.", "danger")
    return render_template("auth/login.html")


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.home"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("user.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            db.session.add(
                PasswordResetToken(
                    user_id=user.id,
                    token=token,
                    expires_at=datetime.now(timezone.utc) + timedelta(hours=2),
                )
            )
            db.session.commit()
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            sent = send_email(
                "SmartPark password reset",
                user.email,
                f"Use this link to reset your password (valid 2 hours):\n{reset_url}",
            )
            if not sent:
                flash(f"Email is not configured. Use this reset link now: {reset_url}", "warning")
            else:
                flash("If that account exists, a reset link has been sent.", "success")
        else:
            flash("If that account exists, a reset link has been sent.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    record = PasswordResetToken.query.filter_by(token=token, used=False).first()
    now = datetime.now(timezone.utc)
    if not record or (record.expires_at.replace(tzinfo=timezone.utc) if record.expires_at.tzinfo is None else record.expires_at) < now:
        flash("This reset link is invalid or has expired.", "danger")
        return redirect(url_for("auth.forgot_password"))
    if request.method == "POST":
        password = request.form.get("password", "")
        if len(password) < 8 or password != request.form.get("confirm_password", ""):
            flash("Use 8+ characters and matching passwords.", "danger")
        else:
            user = db.session.get(User, record.user_id)
            user.set_password(password)
            record.used = True
            db.session.commit()
            flash("Password updated. You can sign in now.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html")
