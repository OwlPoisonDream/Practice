from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import email_validator
from app.models import User

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
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

class ResetPasswordRequestForm(FlaskForm): # Форма востоновление пароля 
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class PersonalForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()]) #ФИО
    birthDAy = StringField('ФИО', validators=[DataRequired()])# Дата рождения 
    passport = StringField('ФИО', validators=[DataRequired()])# номер паспорта
    passportData = StringField('ФИО', validators=[DataRequired()])# дата выдачи 
    passportBy = StringField('ФИО', validators=[DataRequired()])# кем выдан паспорт
    passportCod = StringField('ФИО', validators=[DataRequired()])# код подразделения
    nickname = StringField('ФИО', validators=[DataRequired()]) # прозвище
    link_vk = StringField('ФИО', validators=[DataRequired()]) # ссылка на вк
    inn = StringField('ФИО', validators=[DataRequired()]) # инн
    bank_details = StringField('ФИО', validators=[DataRequired()]) # реквизиты банка  
    bankName = StringField('ФИО', validators=[DataRequired()]) # название банка
    phone_number = StringField('Номер телефона', validators=[DataRequired()]) # номер телефона

