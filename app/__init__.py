from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
"""
This script simply creates 
the application object (of class Flask) and then imports the views module

"""

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#This import is at the bottom of the file to avoid circular imports
from app import views, models