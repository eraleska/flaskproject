from sqlalchemy.orm import backref

from app import db
from app import login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(128), nullable=True)
    group = db.relationship('Group', backref=backref('groups', lazy='dynamic'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    posts = db.relationship('Posts', backref='poster')
    age = db.Column(db.Integer)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '{}'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(10000), index=True, unique=True)

    def __repr__(self):
        return 'Group - {}'.format(self.name)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    #author = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post - {}'.format(self.title)
