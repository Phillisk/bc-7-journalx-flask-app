# Import flask and template operators
from flask import Flask, render_template

# Import extensions e.g. SQLAlchemy, flask-login
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers and flask_migrate for migrations
db = SQLAlchemy(app)


# define login manager
lm = LoginManager()
lm.init_app(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()



