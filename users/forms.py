from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
import re


# Validator method to validate password using regex
def validate_password(form, field):
    p = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')
    if not p.match(field.data):
        raise ValidationError("Password should include at least 1 digit, 1 special character, 1 lowercase and 1 "
                              "uppercase letter.")


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
    phone = StringField(validators=[DataRequired()])
    company = StringField(validators=[DataRequired()])
    company_website = StringField(validators=[DataRequired()])
    logo = FileField(default='/static/img/default.jpeg') # TODO: TEST IF THIS WORKS
    submit = SubmitField()