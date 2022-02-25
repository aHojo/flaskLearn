from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from esportscompanyblog.models.models import User, BlogPost
from esportscompanyblog.users.forms import RegistrationForm, UpdateUserForm, LoginForm
from esportscompanyblog.users.picture_handler import add_profile_pic
from esportscompanyblog import db


users = Blueprint('users', __name__)

# register user
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    # print("HERE", form.email.data, form.validate_on_submit(), form.errors, form.password.data, form.password_cmp.data)
    if form.validate_on_submit():
        # print("HERE 2")
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        # user.create()
        flash("Thanks for registering!")
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# login view
@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(email=form.email.data)

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Login Success!")

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html',form=form)

# logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))

# account (update userForm)
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form =UpdateUserForm()

    print("Here", form.errors, form.validate_on_submit())

    if form.validate_on_submit():

        print(form.errors, form.picture.data)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
            print(current_user.profile_image)
        current_user.username = form.username.data
        current_user.email = form.email.data

        # current_user.update()
        db.session.commit()
        flash("User account updated!")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


# user's list of Blogs
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)

    user = User.get_by_username(username)
    # Because we set backref to author
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)

