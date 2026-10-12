"""Form validation for the SCAM Don't CRAM website."""

from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length


class ReviewForm(FlaskForm):
    """Validate review inputs and provide CSRF protection."""

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=1, max=50),
        ],
    )

    rating = SelectField(
        "Rating",
        choices=[
            ("5", "★★★★★ - 5"),
            ("4", "★★★★☆ - 4"),
            ("3", "★★★☆☆ - 3"),
            ("2", "★★☆☆☆ - 2"),
            ("1", "★☆☆☆☆ - 1"),
        ],
        validators=[DataRequired()],
    )

    comment = TextAreaField(
        "Your Review",
        validators=[
            DataRequired(),
            Length(min=5, max=500),
        ],
    )
