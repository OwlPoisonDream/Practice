from tkinter.tix import Select
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import email_validator
from app.models import User

class LoginForm(FlaskForm): # Форма для логина с запоминанием пользователя
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("remember Me")
    submit = SubmitField()
    

class RegistrationForm(FlaskForm): # Форма регистрации
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField(
        'repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')

    def validate_username(self, username): #Проверка на несовпадение имён пользователя
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя пользователя.')

    def validate_email(self, email): #проверка на несовпадение электронных почт
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой адрес электронной почты.')

class ResetPasswordRequestForm(FlaskForm): # Форма восстановления пароля 
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm): # Форма сброса пароля
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class PersonalForm(FlaskForm): # Форма для заполнения таблицы users_Data
    name = StringField('ФИО', validators=[]) #ФИО
    nickname = StringField('Прозвище', validators=[]) # прозвище
    link_vk = StringField('Ссылка на ВК', validators=[]) # ссылка на вк
    birthDAy = StringField('Дата Рождения', validators=[])# Дата рождения 
    passport = StringField('Номер паспорта', validators=[])# номер паспорта
    passportData = StringField('Дата выдачи ', validators=[])# дата выдачи 
    passportBy = StringField('Кем выдан паспорт', validators=[])# кем выдан паспорт
    passportCod = StringField('Код подразделения', validators=[])# код подразделения
    inn = StringField('ИНН', validators=[]) #инн
    bank_details = StringField('Реквизиты банка ', validators=[]) # реквизиты банка  
    bankName = StringField('Название банка', validators=[]) # название банка
    phone_number = StringField('Номер телефона', validators=[]) # номер телефона
    tags = SelectMultipleField("Специальность",choices=[("Сценарист","Сценарист"), # Выпадающий список с несколькими вариантами
                                                ("Раскадровщик","Раскадровщик"),
                                                ("Черновая анимация","Черновая анимация"),
                                                ("Клин","Клин"),
                                                ("Фоновик","Фоновик"),
                                                ("3D-шник","3D-шник"),
                                                ("Композер","Композер"),
                                                ("Лейаут","Лейаут"),
                                                ("Художник общего профиля","Художник общего профиля"),
                                                ("Монтажер","Монтажер"),
                                                ("Оператор","Оператор"),
                                                ("Актёр озвучки","Актёр озвучки"),
                                                ("Саунд-дизайнер","Саунд-дизайнер"),
                                                ("Композитор","Композитор"),
                                                ("Сведение и чистка звука","Сведение и чистка звука"),
                                                ("Бухгалтер","Бухгалтер"),
                                                ("Юрист","Юрист"),
                                                ("Менеджер","Менеджер"),
                                                ("Шрифтовик","Шрифтовик"),
                                                ("Супервайзер","Супервайзер"),
                                                ("Режиссёр","Режиссёр"),
                                                ("Программист","Программист")], validators=[]) #Теги, отображающие специальности человека
    submit = SubmitField('Изменить данные')

class CreateProject(FlaskForm):# создание проекта
    projectName = StringField('Имя проекта', validators=[DataRequired()])# имя проекта
    descProject = StringField('Описание', validators=[DataRequired()])# описание проекта 
    linkDisk = StringField('ссылка на гугл диск', validators=[DataRequired()])# ссылка на гугл диск
    submit = SubmitField('+ Создать проект')

class CreateTask(FlaskForm):# создание задачи
    idUser = StringField("ID пользователя", validators=[DataRequired()]) #id пользователя
    idProject = StringField('Id проекта', validators=[DataRequired()])  # id проекта. Берёт из таблицы project
    nameTask = StringField('Имя задачи', validators=[DataRequired()])# имя задачи
    descTask = StringField('Описание задачи', validators=[DataRequired()])# Описание задачи
    timeTask = StringField('время выполнения', validators=[DataRequired()])# время выполнения
    manyTask = StringField('сколько заплатят', validators=[DataRequired()])# деньги за задачу
    linkDisk = StringField('ссылка на гугл диск', validators=[DataRequired()])# ссылка на гугл диск
    submit = SubmitField('Создать задачу')

class ChangeTask(FlaskForm):# изменение задачи
    id = StringField("Id задачи", validators=[DataRequired()]) #ID изменяемой задачи
    idUser = StringField("ID пользователя", validators=[DataRequired()]) #id пользователя
    idProject = StringField('Id проекта', validators=[DataRequired()])  # id проекта. Берёт из таблицы project
    nameTask = StringField('Имя задачи', validators=[DataRequired()])# имя задачи
    descTask = StringField('Описание задачи', validators=[DataRequired()])# Описание задачи
    timeTask = StringField('время выполнения', validators=[DataRequired()])# время выполнения
    manyTask = StringField('сколько заплатят', validators=[DataRequired()])# деньги за задачу
    statusСompleted = StringField('Статус выполнения', validators=[DataRequired()]) # Статус выполнения
    receipt = StringField('Чек', validators=[DataRequired()]) # Чек за работу
    linkDisk = StringField('ссылка на гугл диск', validators=[DataRequired()])# ссылка на гугл диск
    submit = SubmitField('Изменить задачу')
