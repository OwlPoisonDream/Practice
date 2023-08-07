from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import RadioField, SelectMultipleField, DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime
from app.models import User

now = datetime.now
#images = UploadSet('images', IMAGES)

class LoginForm(FlaskForm): # Форма для логина с запоминанием пользователя
    email = StringField("Почта", validators=[DataRequired()], render_kw={"placeholder": "Электронная почта"})
    password = PasswordField("Пароль", validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
    

class RegistrationForm(FlaskForm): # Форма регистрации
    email = StringField('Почта', validators=[DataRequired(), Email()], render_kw={"placeholder": "Электронная почта"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    password2 = PasswordField(
    'Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username): #Проверка на несовпадение имён пользователя
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя пользователя.')

    def validate_email(self, email): #проверка на несовпадение электронных почт
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой адрес электронной почты.')

class ResetPasswordRequestForm(FlaskForm): # Форма восстановления пароля 
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"placeholder": "Электронная почта"})
    submit = SubmitField('Вспомнить пароль')

class ResetPasswordForm(FlaskForm): # Форма сброса пароля
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})

    submit = SubmitField('Сбросить пароль')

class PersonalForm(FlaskForm): # Форма для заполнения таблицы users_Data
    name = StringField('ФИО', validators=[]) #ФИО
    nickname = StringField('Прозвище', validators=[]) # прозвище
    link_vk = StringField('Ссылка на ВК', validators=[]) # ссылка на вк
    birthDAy = DateField('Дата Рождения', validators=[])# Дата рождения 
    passport = StringField('Номер паспорта', validators=[Length(min = 11, max = 11)], render_kw={"placeholder": "1111 111111"})# номер паспорта
    passportData = DateField('Дата выдачи ', validators=[])# дата выдачи 
    passportBy = StringField('Кем выдан паспорт', validators=[])# кем выдан паспорт
    passportCod = StringField('Код подразделения', validators=[Length(min = 7, max = 7)], render_kw={"placeholder": "111-111"})# код подразделения
    inn = StringField('ИНН', validators=[Length(min = 12, max = 12)], render_kw={"placeholder": "123456789123"}) #инн
    bankAccount = StringField("Счёт пользователя", validators=[]) #Личный счёт пользователя
    bank_details = StringField('Реквизиты банка ', validators=[]) # реквизиты банка  
    bankName = StringField('Название банка', validators=[]) # название банка
    phone_number = StringField('Номер телефона', validators=[Length(min = 11, max = 25)], render_kw={"placeholder": "+7/8"}) # номер телефона
    email = StringField('Email', validators=[Email()]) # почта
    photo = FileField(validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'Images only')
        ])
    tags = SelectMultipleField("Специальность",choices=[("Сценарист","Сценарист"),# специальность
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
    up_ooo = RadioField('ooo', choices=[(1,'Да'),(0,'Нет')])
    address = StringField('Адрес проживания', validators=[]) # адрес пользователя
    ogrn = StringField("ОГРН", validators=[Length(min = 13, max = 13)], render_kw={"placeholder": "1234567891234"})#ОГРН пользователя
    #SelectMultipleField("ООО или ИП",choices= ['Нет','Да'])
    submit = SubmitField('')



class CreateTask(FlaskForm):# создание задачи
    idProject = IntegerField('Id проекта')  # id проекта. Берёт из таблицы project
    nameTask = StringField('Имя задачи', validators=[DataRequired()])# имя задачи
    descTask = StringField('Описание задачи', validators=[DataRequired()])# Описание задачи
    timeTask = DateField('время выполнения', validators=[DataRequired()])# время выполнения
    manyTask = IntegerField('сколько заплатят', validators=[DataRequired()])# деньги за задачу
    linkDisk = StringField('ссылка на гугл диск', validators=[DataRequired()])# ссылка на гугл диск
    idFolder = IntegerField("ID папки", validators=[DataRequired()])
    submit = SubmitField('Создать задачу')

class ChangeTask(FlaskForm):# изменение задачи
    id = IntegerField("Id задачи", validators=[DataRequired()]) #ID изменяемой задачи
    idUser = IntegerField("ID пользователя", validators=[DataRequired()]) #id пользователя
    idProject = IntegerField('Id проекта', validators=[DataRequired()])  # id проекта. Берёт из таблицы project
    nameTask = StringField('Имя задачи', validators=[DataRequired()])# имя задачи
    descTask = StringField('Описание задачи', validators=[DataRequired()])# Описание задачи
    timeTask = DateField('время выполнения', validators=[DataRequired()])# время выполнения
    manyTask = IntegerField('сколько заплатят', validators=[DataRequired()])# деньги за задачу
    statusСompleted = StringField('Статус выполнения', validators=[DataRequired()]) # Статус выполнения
    receipt = StringField('Чек', validators=[DataRequired()]) # Чек за работу
    linkDisk = StringField('ссылка на гугл диск', validators=[DataRequired()])# ссылка на гугл диск
    submit = SubmitField('Изменить задачу')
