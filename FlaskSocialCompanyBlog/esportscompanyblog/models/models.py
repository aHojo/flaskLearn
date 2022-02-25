from datetime import datetime
from esportscompanyblog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(255), nullable=False, default="default_profile.png"
    )
    email = db.Column(db.String(255), unique=True, index=True)
    username = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(128), unique=True, index=True)

    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email, username, password) -> None:
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def __repr__(self):
        return f"Username {self.username}"

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first_or_404()


    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    #     self.email = email
    #     self.username = username
    #     self.profile_image = profile_pic
    #     db.session.commit()



class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # set up in the users class
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.String(255), nullable=False)

    def __init__(self, title, text, user_id) -> None:
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} --- Date {self.date} -- {self.title}"
