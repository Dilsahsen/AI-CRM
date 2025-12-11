from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from extensions import db
from models.user import User
from forms.auth_forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm,
    ResetPasswordForm,
)
from utils.email import (
    send_security_email,
    send_reset_password_email,
    confirm_reset_token,
)

auth_bp = Blueprint("auth", __name__)

failed_attempts = {}
LOCKOUT_TIME = timedelta(minutes=5)   
MAX_ATTEMPTS = 5                    


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password_input = form.password.data
        now = datetime.now()

        info = failed_attempts.get(email)

        if info:
            attempts, last_attempt = info
            if attempts >= MAX_ATTEMPTS and now - last_attempt < LOCKOUT_TIME:
                flash(
                    "You have made too many incorrect attempts. "
                    "Your account has been locked for 5 minutes.",
                    "error",
                )
                return render_template("auth/login.html", form=form)

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password_input):
            if info and now - info[1] < LOCKOUT_TIME:
                attempts = info[0] + 1
            else:
                attempts = 1

            failed_attempts[email] = (attempts, now)

            if attempts >= MAX_ATTEMPTS and user:
                send_security_email(user)

            flash("Wrong email or password.", "error")
            return render_template("auth/login.html", form=form)

        failed_attempts.pop(email, None)

        login_user(user, remember=form.remember_me.data)
        flash("You have logged in successfully.", "success")

        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)

        return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("This email is already registered.", "error")
            return render_template("auth/register.html", form=form)

        user = User(
            name=form.name.data,
            email=email,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()

        if user:
            send_reset_password_email(user)

        flash(
            "If this email address is registered, a password reset link has been sent.",
            "info",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html", form=form)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    email = confirm_reset_token(token)

    if not email:
        flash("The password reset link is invalid or has expired.", "error")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        new_password = form.password.data
        user.set_password(new_password)  
        db.session.commit()

        flash("Your password has been updated successfully. You can log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form)
