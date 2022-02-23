



### VIEW FUNCTIONS -- HAVE FORMS

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/add_owner", methods=["GET", "POST"])
def add_owner():
    form = AddOwnerForm()

    if form.validate_on_submit():
        name = form.name.data
        pup_id = form.pup_id.data

        owner = Owner(name, pup_id)
        db.session.add(owner)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template("add_owner.html", form=form)



if __name__ == '__main__':
    app.run(debug=True)





