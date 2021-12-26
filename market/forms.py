from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, SubmitField, validators
from market.models import User
from wtforms import ValidationError 
class RegisterForm(FlaskForm):

	def validate_username(self, username_to_check):
		#-- Running data check in here instead of inside the function 
		user = User.query.filter_by(username=username_to_check.data).first() 
		if user:
			raise ValidationError("Username exists")

	def validate_email_address(self, email_to_check):
		email_address = User.query.filter_by(email_address=email_to_check.data).first() 
		if email_address:
			raise ValidationError("Email already in use")

	username = StringField(label = "User Name: ", validators=[validators.Length(min=2, max=32), validators.DataRequired()])
	email_address = StringField(label="Email: ", validators=[validators.Email(), validators.DataRequired()])
	password_1 = PasswordField(label = "Password: ", validators=[validators.Length(min=6), validators.DataRequired()]) 
	password_2 = PasswordField(label = "Confirm password: ", validators=[validators.EqualTo("password_1"), validators.DataRequired()])
	submit = SubmitField(label = "Create My Account: ")


class LoginForm(FlaskForm):
	username = StringField(label="User Name: ", validators=[validators.DataRequired()])
	password = PasswordField(label="Password: ", validators=[validators.DataRequired()])
	submit = SubmitField(label = "Login: ")


class PurchaseItemForm(FlaskForm):
	submit = SubmitField(label = "Purchase")


class SellItemForm(FlaskForm):
	submit = SubmitField(label = "Sell")
