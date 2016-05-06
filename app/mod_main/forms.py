from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as StringField and BooleanField (optional)
from wtforms import SubmitField, StringField, TextAreaField

# Import Form validators
from wtforms.validators import DataRequired

# import models


class JournalEntryForm(Form):
    """
    This form will be used to create a new journal entry
    """
    title = StringField("Title",  [DataRequired(message='Please enter the title to continue.')])
    body = TextAreaField("Body")
    tags = StringField("Tags")
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
