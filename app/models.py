from . import db
from flask.ext.login import UserMixin, AnonymousUserMixin
from datetime import datetime


class ScrapeCount(db.Model):
    __tablename__ = 'scrapecounts'
    id = db.Column(db.Integer, primary_key=True)
    websitename = db.Column(db.String(200))
    count = db.Column(db.Integer)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), unique=True, index=True)
    username = db.Column(db.String(70), unique=True, index=True)
