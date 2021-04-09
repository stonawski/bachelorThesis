from reapp import db
from reapp import loginManager
from flask_login import UserMixin


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    profilePic = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    saved = db.relationship('Saved', lazy=True)

    def __repr__(self):
        return f"User('{ self.username }', '{self.email}', '{self.profilePic}')"

class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    unqNum = db.Column(db.String(50), unique=True, nullable=False)
    add = db.Column(db.String(100), unique=True, nullable=False)
    loc = db.Column(db.String(80), unique=True, nullable=False)
    pr = db.Column(db.String(50), unique=True, nullable=False)
    inf = db.Column(db.String(150), unique=True, nullable=False)