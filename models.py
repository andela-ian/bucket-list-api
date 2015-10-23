from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


class User(Base):
    __tablename__ = "users"
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    bucketlists = db.relationship(
                "BucketList",
                order_by="BucketList.id")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_valid_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username


class Session(Base):
    __tablename__ = "sessions"
    user_id = db.Column(db.Integer)
    token = db.Column(db.String(256))


class BucketList(Base):
    __tablename__ = 'bucketlists'
    name = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")

    bucketlistitems = db.relationship(
                "BucketListItem")

    def __init__(self, created_by, name):
        self.created_by = created_by
        self.name = name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by,
            "user": self.user.id,
            "bucketlistitems": self.bucketlistitems
        }

    @staticmethod
    def for_logged_user(user_id):
        query_result = db.session\
                         .query(BucketList)\
                         .filter_by(created_by=user_id).all()
        return query_result or 'No bucketlist items were found'

    def __repr__(self):
        return "<BucketList(bucketlist='%s')>" % self.name


class BucketListItem(Base):
    __tablename__ = "bucketlistitems"
    name = db.Column(db.String(256), nullable=False)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))

    def __init__(self, bucketlist_id, name, done=False):
        self.bucketlist_id = bucketlist_id
        self.name = name
        self.done = done
