"""Forms and input validation for SCAM Don't CRAM."""

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
)


class ReviewForm(FlaskForm):
    """Validate student reviews before storing them."""

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=1, max=50),
        ],
    )

    rating = IntegerField(
        "Rating",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=5),
        ],
    )

    comment = TextAreaField(
        "Review",
        validators=[
            DataRequired(),
            Length(min=5, max=500),
        ],
    )
