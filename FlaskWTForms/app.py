from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import  FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    DateTimeField,
    RadioField,
    SelectField,
    TextAreaField,
    )
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "kairihojo"

class InfoForm(FlaskForm):

    breed = StringField("What Breed are you?")
    submit = SubmitField("Submit")

class InfoForm2(FlaskForm):
    breed = StringField("What field are you?", validators=[DataRequired()])
    neutered = BooleanField("Have you been neutered?")
    mood = RadioField("Please choose your mood: ", choices=[('mood_one', "Happy"), ('mood_two', 'Excited')])
    food_choice = SelectField(u'Pick your favorite food: ', choices=[('chi', 'Chicken'), ('bf', 'beef'), ('ca', 'Candy')])
    feedback = TextAreaField()
    submit = SubmitField('Submit')

@app.route('/', methods=["GET", "POST"])
def index():  # put application's code here
    breed = False

    form = InfoForm()

    if form.validate_on_submit():
        flash("You just clicked the button!")
        breed = form.breed.data
        form.breed.data = ''

    return render_template("index.html", form=form, breed=breed)

@app.route('/form', methods=["GET", "POST"])
def index2():  # put application's code here
    form = InfoForm2()

    if form.validate_on_submit():
        session['breed'] = form.breed.data
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data


        return redirect(url_for('thankyou'))
    return render_template('questions.html', form=form)

@app.route("/thankyou")
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
