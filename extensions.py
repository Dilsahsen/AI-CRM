from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import flash, redirect, url_for, request
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'
login_manager.session_protection = "strong"

@login_manager.unauthorized_handler
def unauthorized():
    if not request.endpoint or 'auth.login' not in request.endpoint:
        flash("⚠️ You must be logged in to view this page.", "warning")
    return redirect(url_for("auth.login"))

















