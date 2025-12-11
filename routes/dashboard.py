from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import os

from extensions import db
from models.customer import Customer
from models.sale import Sale

dashboard_bp = Blueprint("dashboard", __name__)


# --- LOG OKUMA HELPER'LARI (bunlar sende zaten varsa tekrar yazmana gerek yok) ---
def _get_log_path():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, "logs", "auth.log")


def _read_last_lines(path, n=20):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return [line.strip() for line in lines[-n:]]


def _count_warnings_last_24h():
    path = _get_log_path()
    if not os.path.exists(path):
        return 0

    cutoff = datetime.now() - timedelta(hours=24)
    count = 0

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "WARNING" in line or "Too many failed login attempts" in line:
                try:
                    ts_str = line.split(" INFO:")[0]
                    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S,%f")
                    if ts >= cutoff:
                        count += 1
                except Exception:
                    continue

    return count

@dashboard_bp.route("/")
@login_required
def index():
    total_customers = Customer.query.count()

    total_revenue = (
        db.session.query(db.func.coalesce(db.func.sum(Sale.amount), 0.0))
        .filter(Sale.status == "won")
        .scalar()
    )

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_sales = (
        Sale.query.filter(
            Sale.status == "won",
            Sale.sale_date >= thirty_days_ago,
        ).count()
    )

    total_deals = Sale.query.count()
    won_deals = Sale.query.filter_by(status="won").count()
    if total_deals > 0:
        win_rate = round((won_deals / total_deals) * 100, 1)
    else:
        win_rate = 0.0

    recent_customers = (
        Customer.query.order_by(Customer.created_at.desc()).limit(5).all()
    )

    log_path = _get_log_path()
    recent_logs = _read_last_lines(log_path, n=10)
    warnings_24h = _count_warnings_last_24h()

    sales_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    sales_values = [100, 200, 150, 300, 250, 400, 350]

    return render_template(
        "dashboard.html",
        user=current_user,
        total_customers=total_customers,
        total_revenue=total_revenue,
        recent_sales=recent_sales,
        win_rate=win_rate,
        recent_customers=recent_customers,
        recent_logs=recent_logs,
        warnings_24h=warnings_24h,
        sales_labels=sales_labels,
        sales_values=sales_values,
    )







