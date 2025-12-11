
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from extensions import db
from models.sale import Sale
from models.customer import Customer
from forms.sale_forms import SaleForm

sales_bp = Blueprint("sales", __name__)

@sales_bp.route("/", methods=["GET"])
@login_required
def list_sales():
    sales = (
        Sale.query
        .order_by(Sale.sale_date.desc())
        .all()
    )
    return render_template("sales/list.html", sales=sales)

@sales_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_sale():
    form = SaleForm()
    form.set_customer_choices()  
    if form.validate_on_submit():
        sale = Sale(
            customer_id=form.customer_id.data,
            amount=form.amount.data,
            currency=form.currency.data,
            status=form.status.data,
            sale_date=form.sale_date.data,
            notes=form.notes.data,
        )
        db.session.add(sale)
        db.session.commit()
        flash("Sale created successfully.", "success")
        return redirect(url_for("sales.list_sales"))

    return render_template("sales/add.html", form=form)

@sales_bp.route("/<int:sale_id>/edit", methods=["GET", "POST"])
@login_required
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)

    form = SaleForm(obj=sale)
    form.set_customer_choices(selected_id=sale.customer_id)

    if form.validate_on_submit():
        sale.customer_id = form.customer_id.data
        sale.amount = form.amount.data
        sale.currency = form.currency.data
        sale.status = form.status.data
        sale.sale_date = form.sale_date.data
        sale.notes = form.notes.data

        db.session.commit()
        flash("Sale updated successfully.", "success")
        return redirect(url_for("sales.list_sales"))

    return render_template("sales/edit.html", form=form, sale=sale)

@sales_bp.route("/<int:sale_id>/delete", methods=["POST"])
@login_required
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash("Sale deleted.", "info")
    return redirect(url_for("sales.list_sales"))
