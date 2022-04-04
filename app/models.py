# здесь находятся модели класса
from werkzeug.security import generate_password_hash,  check_password_hash # для создание хеша паролей
from flask_login import  UserMixin 
import jwt
from time import time
from app import db, email,login_manager,app


@login_manager.user_loader # загрузка пользователя
def load_user(id):
    return db.session.query(User).get(id)


# Модель User  - отображение таблицы users в БД 
class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key =True) #id
    email = db.Column(db.String(20), nullable=False) # эмаил
    password_hash = db.Column(db.String(100), nullable=False) # пароль
    who  = db.Column(db.Integer)# 0 - user, 1 - showrunner, 2- admin
    pr = db.relationship('Users_Data', backref='user', uselist=False) #Связываем таблицу User с таблицей Users_Data, где первая - родитель, вторая - наследует

    def __reduce_ex__(self): # id пользователя и его почта 
        return "<{}{}>".format(self.id, self.email)

    def check_password(self,  password): # проверка пароля от пользователя и хэш
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600): #сброс пароля
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token): #подтверждение сброса пароля
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
        
    def set_password(self, password):# ввод пароля в виде хеша 
	    self.password_hash = generate_password_hash(password)



# Модель Tasks  - отображение таблицы task в БД 
class Tasks(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)#id задачи
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'))  # id пользователя. Берёт из таблицы user
    idProject = db.Column(db.Integer, db.ForeignKey('projects.id'))  # id проекта. Берёт из таблицы project
    nameTask = db.Column(db.String(255))# имя задачи
    descTask = db.Column(db.String(255))# Описание задачи
    timeTask = db.Column(db.String(255))# время выполнения
    manyTask = db.Column(db.String(255))# деньги за задачу
    statusСompleted = db.Column(db.String(255))#статус выполнения
    receipt = db.Column(db.Float)# проверка чека
    linkDisk = db.Column(db.String(255))# ссылка на диск

# Модель Project  - отображение таблицы projects в БД 
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)# id проекта
    projectName = db.Column(db.String(255))# имя проекта
    descProject = db.Column(db.String(255))# описание проекта 
    linkDisk = db.Column(db.String(255))# ссылка на гугл диск



class Users_Data(db.Model):
    __tablename__ = 'users_Data'

    id = db.Column(db.Integer, primary_key =True) #id
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'))  # id пользователя. Берёт из user
    name = db.Column(db.String(100), nullable=True) #ФИО
    nickname = db.Column(db.String(20), nullable=True) # прозвище
    link_vk = db.Column(db.String(50), nullable=True) # ссылка на вк
    birthDAy = db.Column(db.String(100), nullable=True)# Дата рождения 
    passport = db.Column(db.String(100), nullable=True)# номер паспорта
    passportData = db.Column(db.String(100), nullable=True)# дата выдачи 
    passportBy = db.Column(db.String(100), nullable=True)# кем выдан паспорт
    passportCod = db.Column(db.String(100), nullable=True)# код подразделения
    inn = db.Column(db.String(12), nullable=True) # инн
    bank_details = db.Column(db.String(100), nullable=True) # реквизиты банка  
    bankName = db.Column(db.String(100), nullable=True) # название банка
    phone_number = db.Column(db.String(11), nullable=True) # номер телефона
