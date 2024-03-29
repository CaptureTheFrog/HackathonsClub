from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, BooleanField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
import re


# Validator method to validate password using regex
def validate_password(form, field):
    p = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')
    if not p.match(field.data):
        raise ValidationError("Password should include at least 1 digit, 1 special character, 1 lowercase and 1 "
                              "uppercase letter.")


# Validator method to validate phone number using regex
def validate_phone(form, field):
    # XXXX-XXX-XXXX
    p = re.compile(r'\d{4}-\d{3}-\d{4}')
    if not p.match(field.data):
        raise ValidationError("Phone number must be in the format XXXX-XXX-XXXX.")


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class UserRegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(),
                                         Length(min=6, max=20, message="Password must be between 6 and 20 characters "
                                                                       "in length"),
                                         validate_password])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', 'Both password fields must be '
                                                                                     'equal.')])
    submit = SubmitField()


class SponsorRegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(),
                                         Length(min=6, max=20, message="Password must be between 6 and 20 characters "
                                                                       "in length"),
                                         validate_password])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', 'Both password fields must be '
                                                                                     'equal.')])
    phone = StringField(validators=[DataRequired(), validate_phone])
    company = StringField(validators=[DataRequired()])
    company_website = StringField(validators=[DataRequired()])
    logo = FileField(default='/static/img/default.jpeg')  # TODO: TEST IF THIS WORKS
    submit = SubmitField()


class PasswordForm(FlaskForm):
    current_password = PasswordField(id='password', validators=[DataRequired()])
    show_password = BooleanField('Show password', id='check')
    new_password = PasswordField(validators=[DataRequired(),
                                             Length(min=6, max=20,
                                                    message="Must be between 6 and 20 characters in length"),
                                             validate_password])
    confirm_new_password = PasswordField(validators=[DataRequired(),
                                                     EqualTo('new_password',
                                                             message='Both new password fields must be equal.')])
    submit = SubmitField('Change Password')


class CreateEventForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    start_date = DateField(validators=[DataRequired()])
    end_date = DateField(validators=[DataRequired()])
    location = StringField()
    website = StringField()
    submit = SubmitField()
