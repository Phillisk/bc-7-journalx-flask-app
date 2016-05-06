# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as StringField and BooleanField (optional)
from wtforms import PasswordField, BooleanField, SubmitField, validators, StringField

# Import Form validators
from wtforms.validators import Email, DataRequired

# import models
from app.mod_main.models import User


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



