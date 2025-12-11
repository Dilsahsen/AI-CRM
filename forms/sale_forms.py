from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from models.customer import Customer


class SaleForm(FlaskForm):
    customer_id = SelectField("Customer", coerce=int, validators=[DataRequired()])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0)])
    currency = StringField("Currency", default="USD", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=[("open", "Open"), ("won", "Won"), ("lost", "Lost")],
        validators=[DataRequired()],
    )
    sale_date = DateField("Sale Date", validators=[Optional()])
    notes = StringField("Notes", validators=[Optional()])
    submit = SubmitField("Save")

    def set_customer_choices(self, selected_id=None):
        
        customers = Customer.query.order_by(Customer.name).all()
        self.customer_id.choices = [(c.id, c.name) for c in customers]

        if selected_id is not None:
            self.customer_id.data = selected_id