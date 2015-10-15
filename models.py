from flask.ext.sqlalchemy import SQLAlchemy
from flask import session, app


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_valid_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username


class BucketList(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(
                "User",
                backref=db.backref('bucketlists', order_by=id))

    def __init__(self, user_id, todo):
        self.user_id = user_id
        self.todo = todo

    @staticmethod
    def for_logged_user(user_id):
        query_result = db.session\
                         .query(BucketList)\
                         .filter_by(user_id=user_id).all()
        return query_result or 'No bucketlist items were found'

    def __repr__(self):
        return "<BucketList(bucketlist='%s')>" % self.todo
