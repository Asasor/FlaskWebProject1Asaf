from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class QueryFormStructure(FlaskForm):
    """This class contains the names of all the fields in the form"""
    name = StringField('Enter Team Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserRegistrationFormStructure(FlaskForm):
    FirstName = StringField('First Name:   ', validators=[DataRequired()])
    LastName = StringField('Last Name:   ', validators=[DataRequired()])
    PhoneNum = StringField('Phone Number:   ', validators=[DataRequired()])
    EmailAddr = StringField('Email:   ', validators=[DataRequired()])
    username = StringField('User name:   ', validators=[DataRequired()])
    password = StringField('Pass word:   ', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginFormStructure(FlaskForm):
    username = StringField('User name:   ', validators=[DataRequired()])
    password = StringField('Pass word:   ', validators=[DataRequired()])
    submit = SubmitField('Submit')
