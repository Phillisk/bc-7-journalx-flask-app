from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from flask.ext.login import current_user, login_required, logout_user, login_user
from app import db, lm, app
from app.mod_auth.forms import LoginForm, SignupForm, JournalEntryForm, SearchForm
from app.mod_auth.models import User, Journal, Tag
from config import MAX_SEARCH_RESULTS

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
        return redirect(url_for('auth.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('auth.profile'))

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
            newuser = User(form.firstname.data, form.lastname.data, form.username.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        return render_template('auth/signup.html', form=form)


@mod_auth.route('/logout/')
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('auth.index'))


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
    user = g.user

    if user is None:
        return redirect(url_for('auth.index'))
    else:
        # get the posts for the user. use python query
        entries = Journal.query.filter_by(user_id=current_user.id).order_by(Journal.date_created.desc())

        # pass the posts as a context in the render_template below
        return render_template('auth/profile.html', entries=entries, user=user)


@mod_auth.route('/journalentry/', methods=['GET', 'POST'])
@login_required
def JournalEntry():
    """
    view for new posts
    """
    form = JournalEntryForm()

    if request.method == 'POST':
        newentry = Journal(title=form.title.data,
                           body=form.body.data,
                           tags=form.tags.data,
                           user_id=current_user.id)

        db.session.add(newentry)
        db.session.commit()
        flash('You have successfully added an entry')
        return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        return render_template('auth/journalentry.html', form=form)


@mod_auth.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view_entry(id):

    journal_entry = Journal.query.get_or_404(id)
    user =  current_user

    return render_template('auth/viewentry.html', journal_entry=journal_entry, user=user)


@mod_auth.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def update_entry(id):
    journal_entry = Journal.query.get_or_404(id)
    if current_user.id != journal_entry.user_id:
        abort(403)

    form = JournalEntryForm(obj=journal_entry)

    if request.method == 'POST':
        journal_entry.title = form.title.data
        journal_entry.body = form.body.data
        journal_entry.tags = form.tags.data
        journal_entry.user_id = current_user.id

        db.session.add(journal_entry)
        db.session.commit()

        return redirect(url_for('auth.profile'))
    return render_template('auth/edit.html', form=form)


@mod_auth.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    journal_entry = Journal.query.get_or_404(id)
    if current_user.id != journal_entry.user_id:
        abort(403)

    db.session.delete(journal_entry)
    return render_template('auth/delete.html', journal_entry=journal_entry)

@mod_auth.route('/deleting/<int:id>', methods=['GET', 'POST'])
@login_required
def deleting(id):
    journal_entry = Journal.query.get_or_404(id)
    db.session.delete(journal_entry)
    db.session.commit()
    return redirect(url_for('auth.profile'))
    # return render_template('auth/delete.html', journal_entry=journal_entry)



@mod_auth.route('/search/', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('auth.index'))
    return redirect(url_for('auth.search_results', query=g.search_form.search.data))


@mod_auth.route('/search_results/<query>')
@login_required
def search_results(query):

    results = Journal.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    # import pdb; pdb.set_trace()

    return render_template('auth/search_results.html', query=query, results=results)




