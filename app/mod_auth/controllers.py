#Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from flask.ext.login import current_user, login_required

# Import password / encryption helper tools

from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db, lm

# Import module forms
from app.mod_auth.forms import LoginForm, SignupForm, NewPostForm

# Import module models (i.e. User)
from app.mod_auth.models import User, Journal


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('auth/login.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('auth.profile'))
         
    elif request.method == 'GET':

        return render_template("auth/login.html", form=form)


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    signup view
    """
    form = SignupForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('auth/signup.html', form=form)
        else:   
            newuser = User(form.firstname.data, form.lastname.data, form.username.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        return render_template('auth/signup.html', form=form)

# @app.route('/logout')
# def signout():

#     if 'email' not in session:
#     return redirect(url_for('login'))

#     session.pop('email', None)
#     return redirect(url_for('home'))


@mod_auth.route('/index/')
def index():
    return render_template('auth/index.html')


@mod_auth.route('/profile/')
@login_required
def profile():
    """
    Takes username and matches with journals:
    returns the posts by that user
    """
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    else:
        user = User.query.filter_by(email=session['email']).first()

        if user is None:
            return redirect(url_for('auth.index'))

        else:
            # get the posts for the user. use python query
            posts = Journal.query.filter_by(user_id=user.id)

            # pass the posts as a context in the render_template below
            return render_template('auth/profile.html', posts=posts)


@mod_auth.route('/newpost/', methods=['GET', 'POST'])
def NewPost():
    """
    view for new posts
    """
    form = NewPostForm(request.form)

    if request.method == 'POST':
            newpost = Journal(title=form.title.data,
                              body=form.body.data,
                              tags=form.tags.data,
                              user_id=current_user._get_current_object())
            db.session.add(newpost)
            db.session.commit()

            return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        return render_template('auth/newpost.html', form=form)



