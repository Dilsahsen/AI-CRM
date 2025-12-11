
from datetime import datetime
from extensions import db

class Sale(db.Model):
    __tablename__ = "sale"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.id"),
        nullable=False
    )

    amount = db.Column(db.Float, nullable=False)  # satış tutarı (ör: 199.99)
    currency = db.Column(db.String(10), default="USD")  # şimdilik opsiyonel
    status = db.Column(
        db.String(20),
        default="completed"
    ) 

    sale_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Sale id={self.id} customer_id={self.customer_id} amount={self.amount}>"
