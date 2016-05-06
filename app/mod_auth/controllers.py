from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from flask.ext.login import current_user, logout_user, login_user
from app import db, lm, app
from app.mod_auth.forms import LoginForm, SignupForm
from app.mod_main.forms import SearchForm
from app.mod_main.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.search_form = SearchForm()


# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('main.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html', form=form)


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
            newuser = User(form.firstname.data,
                           form.lastname.data,
                           form.username.data,
                           form.email.data,
                           form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('main.profile'))

    elif request.method == 'GET':
        return render_template('auth/signup.html', form=form)


@mod_auth.route('/logout/')
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('main.index'))




