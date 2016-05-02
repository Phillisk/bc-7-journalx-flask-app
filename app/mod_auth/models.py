# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
#use the werkzeug security options to store a salted password
from werkzeug import generate_password_hash, check_password_hash

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'user'

    # User Names
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)

    # Identification Data: email & password
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # New instance instantiation procedure
    def __init__(self, firstname, lastname, username, email, password):

        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email    = email
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % (self.username) 

    #generates a hash for storing password
    def set_password(self, password_string):
        self.password = generate_password_hash(password_string)

    #checks if password is in db
    def check_password(self, password_string):
        return check_password_hash(self.password, password_string)

# class  Journal(Base):
#     """this is the  model for journals """
#     __tablename__ = 'journals'

#     #journal details
#     title = db.Column(db.String(200), nullable=False)
#     body = db.Column(db.String(1000), nullable=False)
#     tags = db.Column(db.String(50), nullable=True)




