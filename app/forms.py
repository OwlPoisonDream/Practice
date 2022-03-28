from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import email_validator
from app.models import User

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password_hash = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("remember Me")
    submit = SubmitField()
    

class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField(
        'repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя пользователя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой адрес электронной почты.')