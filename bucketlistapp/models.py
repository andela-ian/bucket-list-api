from transformers.transform_to_dict import list_object_transform
import hashlib
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    """Base model that other models inherit from
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


class User(Base):
    """User model that maps to users table
    """
    __tablename__ = "users"
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    bucketlists = db.relationship(
                "BucketList",
                order_by="BucketList.id")

    def __init__(self, username, password):
        """Initialize with <username> and <password>
        """
        self.username = username
        self.password = hashlib.sha512(password).hexdigest()

    def is_valid_password(self, password):
        """Validates user password
        """
        return self.password == hashlib.sha512(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username


class Session(Base):
    """Maps to session table that stores JWTs.
    """
    __tablename__ = "sessions"
    user_id = db.Column(db.Integer)
    token = db.Column(db.String(256))


class BucketList(Base):
    """Maps to the bucketlist table
    """
    __tablename__ = 'bucketlists'
    name = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")

    bucketlistitems = db.relationship(
                "BucketListItem")

    def __init__(self, created_by, name):
        """Initialize with <creator>, <name>
        """
        self.created_by = created_by
        self.name = name

    def to_json(self):
        """Converts model object into dict to ease Serialization
        """
        return {
            "id": self.id,
            "name": self.name,
            "bucketlistitems": list_object_transform(self.bucketlistitems),
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "created_by": self.created_by,
        }

    @staticmethod
    def for_logged_user(user_id):
        """Modifies query result to return records belonging to logged
        user
        """
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
        """Initialize model with <bucketlist_id> and <name>.
        <done> is optional
        """
        self.bucketlist_id = bucketlist_id
        self.name = name
        self.done = done

    def to_json(self):
        """Converts model object into dict to ease Serialization
        """
        return {
            "id": self.id,
            "name": self.name,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "done": self.done,
        }
