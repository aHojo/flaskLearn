from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = StringField("Name of Puppy")
    submit = SubmitField("Add Puppy")

class DelForm(FlaskForm):

    id = IntegerField("ID Number of puppy to Reomove: ")
    submit = SubmitField("Remove Puppy")

class AddOwnerForm(FlaskForm):

    name = StringField("Name of Puppy")
    pup_id = IntegerField("Id of puppy")
    submit = SubmitField("Add Owner")