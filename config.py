"""
This file will contain configurations for the application
"""
# Statement for enabling the development environment
DEBUG = True


# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# define whoosh to implement search
WHOOSH_BASE = os.path.join(BASE_DIR, 'search.db')
MAX_SEARCH_RESULTS = 50
# Define the database - we are working with
# SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
