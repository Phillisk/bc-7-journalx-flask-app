# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, BooleanField, SubmitField, validators, ValidationError

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

#import models
from app.mod_auth.models import User

# Define the login form (WTForms)

class LoginForm(Form):
	"""
	login form
	"""
	email = TextField('Email Address', [Email(),Required(message='Forgot your email address?'),
                validators.Email("Please enter a correct email address.")])
	password = PasswordField('Password', [Required(message='Must provide a password.')])
	remember_me = BooleanField('remember_me', default=False)

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
			return False

class SignupForm(Form):
	"""
	Signup Form
	"""
	firstname = TextField("First name",  [Required(message='Please enter your first name.')])
	lastname = TextField("Last name",  [Required(message='Please enter your last name.')])
	username = TextField("Username",  [Required(message='Please enter your username.')])
	email = TextField("Email",  [Required(message='Please enter your email address.'), 
				validators.Email("Please enter a correct email address.")])
	password = PasswordField('Password', [Required(message='Please enter a password.')])
	confirmpassword = PasswordField('Confirm Password', [Required(message='Please reenter  password.')])
	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	#flask-WTF validate function to ensure the form is filled correctly
	def validate(self):
		if not Form.validate(self):
			return False

		#check if both passwords are equal
		if self.password != self.confirmpassword:
			self.password.errors.append("The password does not match")


		#check if email exists
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken")
			return False
		else:
			return True