import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager



# App Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

#################
# Database Setup

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app=app, db=db)
###################


# LOGIN CONFIG
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "users.login"


from esportscompanyblog.core.views import core
from esportscompanyblog.error_pages.handlers import error_pages
from esportscompanyblog.users.views import users
from esportscompanyblog.blog_posts.views import blog_posts
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)
