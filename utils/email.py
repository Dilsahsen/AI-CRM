
from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from extensions import mail 

def send_security_email(user):
    print(">>> DEBUG: send_security_email CALLED for", user.email)

def send_reset_password_email(user):
    token = generate_reset_token(user.email)

    reset_url = url_for(
        "auth.reset_password",
        token=token,
        _external=True
    )

    print(">>> DEBUG RESET URL:", reset_url)  

    msg = Message(
        subject="Password Reset Request",
        recipients=[user.email],
    )
    msg.body = (
        f"Hello {user.name},\n\n"
        "We received a request to reset your AI-CRM account password.\n"
        f"{reset_url}\n\n"
        "If you did not request a password reset, you can ignore this email.\n\n"
        "AI-CRM Team"
    )
    mail.send(msg)


def _get_serializer():
    secret_key = current_app.config.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY is not set in app config.")
    return URLSafeTimedSerializer(secret_key)

def send_security_email(user):
    try:
        msg = Message(
            subject="⚠️ Suspicious Login Activity Detected",
            recipients=[user.email],
        )
        msg.body = (
            f"Hello {user.name},\n\n"
            "We detected multiple failed login attempts on your account.\n"
            "If this was not you, please change your password immediately.\n\n"
            "For your security, this activity has been logged by our system.\n\n"
            "AI-CRM Security Team"
        )
        mail.send(msg)
    except Exception as e:
        print("Security email could not be sent:", e)

def generate_reset_token(email: str) -> str:
    s = _get_serializer()
    return s.dumps(email, salt="password-reset")


def confirm_reset_token(token: str, max_age: int = 3600) -> str | None:
    s = _get_serializer()
    try:
        email = s.loads(token, salt="password-reset", max_age=max_age)
        return email
    except (BadSignature, SignatureExpired):
        return None


def send_reset_password_email(user):
    try:
        token = generate_reset_token(user.email)
        reset_url = url_for(
            "auth.reset_password",
            token=token,
            _external=True  
        )

        msg = Message(
            subject="Password Reset Request",
            recipients=[user.email],
        )
        msg.body = (
            f"Hello {user.name},\n\n"
            "We received a request to reset your AI-CRM account password.\n"
            "You can reset your password by clicking the link below:\n\n"
            f"{reset_url}\n\n"
            "This link will expire after a limited time (e.g., 1 hour).\n"
            "If you did not request a password reset, you can safely ignore this email.\n\n"
            "AI-CRM Team"
        )
        mail.send(msg)
    except Exception as e:
        print("Reset password email could not be sent:", e)
