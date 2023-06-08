from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FieldList, FormField, \
    RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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
