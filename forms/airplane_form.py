from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired



# WTForm for the airplane form
class AirplaneForm(FlaskForm):
    origin = StringField("Departure city", validators=[DataRequired()])
    destination = StringField("Destination city", validators=[DataRequired()])
    max_price = IntegerField("Max price of trip", validators=[DataRequired()])

    submit = SubmitField("Submit")
