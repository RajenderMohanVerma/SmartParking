from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_

from app import db
from app.models import User

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
