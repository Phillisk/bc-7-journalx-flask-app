# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as StringField and BooleanField (optional)
from wtforms import PasswordField, BooleanField, SubmitField, validators, ValidationError, StringField

# Import Form validators
from wtforms.validators import Email, EqualTo, DataRequired

# import models
from app.mod_auth.models import User


# Define the login form (WTForms)

class LoginForm(Form):
    """
    login form
    """
    email = StringField('Email Address', [Email(),DataRequired(message='Forgot your email address?'),
                                          validators.Email("Please enter a correct email address.")])
    password = PasswordField('Password', [DataRequired(message='Must provide a password.')])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField("Log In")

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)
    #
    # def validate(self):
    #     if not Form.validate(self):
    #         return False
    #
    #     user = User.query.filter_by(email = self.email.data.lower()).first()
    #     if user and user.check_password(self.password.data):
    #         return True
    #     else:
    #         self.email.errors.append("Invalid e-mail or password")
    #         return False


class SignupForm(Form):
    """
    Signup Form
    """
    firstname = StringField("First name",  [DataRequired(message='Please enter your first name.')])
    lastname = StringField("Last name",  [DataRequired(message='Please enter your last name.')])
    username = StringField("Username",  [DataRequired(message='Please enter your username.')])
    email = StringField("Email",  [DataRequired(message='Please enter your email address.'),
                                   validators.Email("Please enter a correct email address.")])
    password = PasswordField('Password', [DataRequired(message='Please enter a password.')])
    confirmpassword = PasswordField('Confirm Password', [DataRequired(message='Please reenter  password.')])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    # flask-WTF validate function to ensure the form is filled correctly
    def validate(self):
        if not Form.validate(self):
            return False

        # check if both passwords are equal
        if self.password != self.confirmpassword:
            self.password.errors.append("The password does not match")

        # check if email exists
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class JournalEntryForm(Form):
    """
    This form will be used to create a new journal entry
    """
    title = StringField("Title",  [DataRequired(message='Please enter the title to continue.')])
    body = StringField("Body")
    tags = StringField("Tags")
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super(JournalEntryForm, self).__init__(*args, **kwargs)


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


