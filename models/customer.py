from extensions import db
from datetime import datetime

from models import interaction

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sales = db.relationship('Sale', backref='customer', lazy=True, cascade="all, delete-orphan")
    interactions = db.relationship('Interaction', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"



