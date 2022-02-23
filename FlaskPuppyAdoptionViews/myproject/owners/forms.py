from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):

    name = StringField("Name of Puppy")
    pup_id = IntegerField("Id of puppy")
    submit = SubmitField("Add Owner")