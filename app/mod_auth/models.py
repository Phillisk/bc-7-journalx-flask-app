from app import db, lm, app
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True


    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


# Define a User model
class User(UserMixin, Base):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    #journals = db.relationship("Journal", backref='author', lazy='dynamic', primaryjoin="User.id == Journal.user_id")

    # New instance instantiation procedure
    def __init__(self, firstname, lastname, username, email, password):

        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.set_password(password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username

    # generates a hash for storing password
    def set_password(self, password_string):
        self.password = generate_password_hash(password_string)

    # checks if password is in db
    def check_password(self, password_string):
        return check_password_hash(self.password, password_string)

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Tag(Base):
    """ This model will create a table for tags"""
    __tablename__ = 'tags'
    id = db.Column(db.Integer)
    tagname = db.Column(db.String(128), primary_key=True )


class Journal(Base):
    """this is the  model for journals """
    __tablename__ = 'journal'
    __searchable__ = ['body', 'title', 'tags']


    # journal details
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    tags = db.Column(db.String(50),  db.ForeignKey('tags.tagname'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    def __init__(self, title, body, tags, user_id):
        self.title = title
        self.body = body
        self.tags = tags
        self.user_id = user_id

    def __repr__(self):
        return '<Journal %r>' % self.title


if enable_search:
        whooshalchemy.whoosh_index(app, Journal)


