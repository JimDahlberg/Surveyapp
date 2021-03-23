from flask_wtf import FlaskForm
from surveyapp.models import HashTable
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import datetime


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        username = HashTable.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = HashTable.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CreateForm(FlaskForm):
    firstName = StringField('First name',
                            validators=[DataRequired(), Length(max=20)])
    lastName = StringField('Last name',
                           validators=[DataRequired(), Length(max=40)])
    depId = StringField('Department ID', validators=[
                        DataRequired(), Length(max=10)])
    accountLevel = SelectField('Account level', choices=[(
        '1', 'Admin'), ('2', 'HR'), ('3', 'Manager'), ('4', 'Employee')],
        validators=[DataRequired()])
    submit = SubmitField('Create Employee')


class AskForm(FlaskForm):
    surveyTitle = StringField('Question title',
                              validators=[DataRequired()])
    surveyQuestion = TextAreaField('Question',
                                   validators=[DataRequired()])
    endDate = DateField('End date', format='%Y-%m-%d',
                        validators=[DataRequired()])
    participantId = StringField('Department',
                                validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_endDate(self, endDate):
        endDate = datetime.datetime.strptime(
            endDate.raw_data[0], '%Y-%m-%d').date()
        if endDate < datetime.date.today():
            raise ValidationError('End date cannot be earlier than today.')


class ResponseForm(FlaskForm):
    response = TextAreaField('Your answer', validators=[DataRequired()])
    submit = SubmitField('Submit')
