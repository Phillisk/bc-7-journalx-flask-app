from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort
from flask.ext.login import login_required, current_user

from app import db
from app.mod_main.forms import JournalEntryForm
from app.mod_main.models import Journal
from config import MAX_SEARCH_RESULTS

mod_main = Blueprint('main', __name__)


@mod_main.route('/index/')
def index():
    return render_template('main/index.html')


@mod_main.route('/profile/')
@login_required
def profile():
    """
    Takes username and matches with journals:
    returns the posts by that user
    """
    user = g.user

    if user is None:
        return redirect(url_for('main.index'))
    else:
        # get the posts for the user. use python query
        entries = Journal.query.filter_by(user_id=current_user.id).order_by(Journal.date_created.desc())

        # pass the posts as a context in the render_template below
        return render_template('main/profile.html', entries=entries, user=user)


@mod_main.route('/journalentry/', methods=['GET', 'POST'])
@login_required
def JournalEntry():
    """
    view for new entries
    """
    form = JournalEntryForm()

    if request.method == 'POST':
            if form.validate_on_submit():
                newentry = Journal(title=form.title.data,
                                   body=form.body.data,
                                   tags=form.tags.data,
                                   user_id=current_user.id)

                db.session.add(newentry)
                db.session.commit()
                flash('You have successfully added an entry')
                return redirect(url_for('main.profile'))
            return render_template('main/journalentry.html', form=form)


    elif request.method == 'GET':
        return render_template('main/journalentry.html', form=form)


@mod_main.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view_entry(id):

    journal_entry = Journal.query.get_or_404(id)
    user =  current_user

    return render_template('main/viewentry.html', journal_entry=journal_entry, user=user)


@mod_main.route('/edit/<int:id>', methods=['GET', 'POST'])
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

        return redirect(url_for('main.profile'))
    return render_template('main/edit.html', form=form)


@mod_main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    journal_entry = Journal.query.get_or_404(id)
    if current_user.id != journal_entry.user_id:
        abort(403)

    db.session.delete(journal_entry)
    return render_template('main/delete.html', journal_entry=journal_entry)

@mod_main.route('/deleting/<int:id>', methods=['GET', 'POST'])
@login_required
def deleting(id):
    journal_entry = Journal.query.get_or_404(id)
    db.session.delete(journal_entry)
    db.session.commit()
    return redirect(url_for('main.profile'))
    # return render_template('auth/delete.html', journal_entry=journal_entry)



@mod_main.route('/search/', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('main.index'))
    return redirect(url_for('main.search_results', query=g.search_form.search.data))


@mod_main.route('/search_results/<query>')
@login_required
def search_results(query):

    results = Journal.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    # import pdb; pdb.set_trace()

    return render_template('main/search_results.html', query=query, results=results)

