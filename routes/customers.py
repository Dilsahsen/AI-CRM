from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.customer import Customer
from forms.customer_forms import CustomerForm

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/")
@login_required

def list_customers():
    customers = (
        Customer.query
        .order_by(Customer.created_at.desc())
        .all()
    )
    return render_template("customers.html", customers=customers)

@customers_bp.route("/add" , methods=["GET", "POST"])
@login_required
def add_customer():
    form = CustomerForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()

        existing = Customer.query.filter_by(email=email).first()
        if existing:
            flash("A customer with this email already exists." , "warning")
            return render_template("customer_add.html" , form=form)

        customer = Customer(
            name = form.name.data.strip(),
            email = email,
            phone = form.phone.data.strip() if form.phone.data else None,
        )

        db.session.add(customer)
        db.session.commit()

        flash("Customer added succesfully." , "success")
        return redirect(url_for("customers.list_cust"))

    return render_template("customer_add.html" , form=form)

@customers_bp.route("/delete/<int:customer_id>")
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()
    
    flash("Customer deleted." , "info")
    return redirect(url_for("customers.list_customers"))