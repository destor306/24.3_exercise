from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, URL, NumberRange, Optional


class CupcakeForm(FlaskForm):
    """Form for Cupcape"""
    flavor = StringField('Flavor', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    rating = FloatField('rating', validators=[
                        DataRequired(), NumberRange(min=1, max=10)])
    image = StringField('Image URL', validators=[Optional()])
