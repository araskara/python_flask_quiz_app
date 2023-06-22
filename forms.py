from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FieldList, FormField, \
    RadioField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=100)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class QuizCreationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description', validators=[Length(max=500)])
    submit = SubmitField('Create Quiz')


class QuForm(FlaskForm):
    title = StringField('Question ID',
                        validators=[DataRequired()])
    content = TextAreaField('Question',
                            validators=[DataRequired()])
    option1 = StringField('option1',
                          validators=[DataRequired()])
    option2 = StringField('option2',
                          validators=[DataRequired()])
    option3 = StringField('option3',
                          validators=[DataRequired()])
    option4 = StringField('option4',
                          validators=[DataRequired()])
    optionCorrect = StringField('optionCorrect',
                                validators=[DataRequired()])

    submit = SubmitField('Publish')


class ChoiceForm(FlaskForm):
    example = RadioField('Label', choices=[('value', 'description'), ('value_two', 'whatever')])
