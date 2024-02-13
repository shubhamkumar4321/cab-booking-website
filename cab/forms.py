from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField,TimeField,DateField,DateTimeField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from cab.models import User
from datetime import datetime



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class Booking_Form(FlaskForm):
    location=StringField(label='Enter Location', validators=[DataRequired()])
    destination=StringField(label='Enter Destination', validators=[DataRequired()])
    dates = DateField('Date', format='%Y-%m-%d', default=datetime.now().date,validators=[DataRequired()])
    times = TimeField('Time', format='%H:%M', default=datetime.now(),validators=[DataRequired()])
    submit = SubmitField(label='Book the Ride')

class VerifyForm(FlaskForm):
    submit = SubmitField(label='Book the Tour')

class CancellationForm(FlaskForm):
    submit = SubmitField(label='Cancel Ride!')
