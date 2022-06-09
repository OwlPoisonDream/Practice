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
    who  = db.Column(db.Integer)# 0 - user, 1 - showrunner, 2- admin, 3 - профиль заблокирован
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
    idUser = db.Column(db.Integer)  # id пользователя. Берёт из таблицы user
    idProject = db.Column(db.Integer)  # id проекта. Берёт из таблицы project
    id_folder = db.Column(db.Integer)# id папки
    nameTask = db.Column(db.String(255))# имя задачи
    descTask = db.Column(db.String(255))# Описание задачи
    timeTask = db.Column(db.String(255))# время выполнения
    manyTask = db.Column(db.String(255))# деньги за задачу
    statusСompleted = db.Column(db.String(255))#статус выполнения
    receipt = db.Column(db.Integer)# проверка чека 0 - чек не нужен,1 - чек еще не прекреплен, 2 - чек прекреплен, 3 - чек проверен   
    linkDisk = db.Column(db.String(255))# ссылка на диск
    
    
# Модель Project  - отображение таблицы projects в БД 
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)# id проекта
    projectName = db.Column(db.String(255))# имя проекта
    descProject = db.Column(db.String(255))# описание проекта 
    linkDisk = db.Column(db.String(255))# ссылка на гугл диск
    linkPoto = db.Column(db.String(255))# ссылка на изображения 

# Модель Users_Projects - отображение таблицы какой пользователь к какой таблице              
class Users_Projects(db.Model):
    __tablename__ = 'user_project'
    id = db.Column(db.Integer, primary_key = True)
    User_id = db.Column(db.Integer, db.ForeignKey('users_Data.id'))# id пользователя. Берёт из таблицы user
    Project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))# id проекта. Берёт из таблицы project
    up = db.relationship('Users_Data', backref='user_project', uselist=False) #Связываем таблицу user с таблицей Users_Projects где первая - родитель, вторая - наследует


# Модель Users_Data - модель для юзера
class Users_Data(db.Model):
    __tablename__ = 'users_Data'

    id = db.Column(db.Integer, primary_key =True) #id
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'),db.ForeignKey('massege.id_user'))  # id пользователя. Берёт из user
    name = db.Column(db.String(100), nullable=True) #ФИО
    nickname = db.Column(db.String(20), nullable=True) # прозвище
    link_vk = db.Column(db.String(50), nullable=True) # ссылка на вк
    birthDAy = db.Column(db.String(100), nullable=True)# Дата рождения 
    passport = db.Column(db.String(100), nullable=True)# номер паспорта
    passportData = db.Column(db.String(100), nullable=True)# дата выдачи 
    passportBy = db.Column(db.String(100), nullable=True)# кем выдан паспорт
    passportCod = db.Column(db.String(100), nullable=True)# код подразделения
    address = db.Column(db.Text, nullable=True)#Адрес проживания 
    bankAccount = db.Column(db.Text, nullable=True)# Личный счёт пользователя
    inn = db.Column(db.String(12), nullable=True) # инн
    bank_details = db.Column(db.String(100), nullable=True) # реквизиты банка  
    bankName = db.Column(db.String(100), nullable=True) # название банка
    phone_number = db.Column(db.String(11), nullable=True) # номер телефона
    tags = db.Column(db.Text, nullable=True)#специализация
    avatar = db.Column(db.String(100), nullable=True)#аватарка пользователя
    up_ooo = db.Column(db.Integer, nullable=True) # проверка ИП и ООО, 0 - нет, 1 - да
    ogrn = db.Column(db.String(13), nullable=True)#ОГРН Пользователя
    chekManager = db.Column(db.Integer, nullable=True) # посмотрел ли профиль менеджер. 0 - профиль не заполне, 1 - профиль на проверке у менеджера, 2 - профиль проверил менеджер
    
# Таблица с документами
class Documents(db.Model):
    __tablename__ = "documents"
    
    id = db.Column(db.Integer, primary_key=True) # id документа
    name = db.Column(db.String(50), nullable=True) # имя документа
    link = db.Column(db.Text, nullable=True)# ссылка на документ
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'))# id usera

# папки
class Folder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True) # id документа
    id_folder = db.Column(db.Integer)# id папки сверху если такая имеется
    id_progect = db.Column(db.Integer)# id проекта
    link = db.Column(db.Text, nullable=True)# ссылка для диска 
    name = db.Column(db.String(50), nullable=True) # имя папки
    color = db.Column(db.String(), nullable=True) # цвет папки

# 
class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=True)

# Таблица чеков
class Check(db.Model):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)# id 
    name = db.Column(db.Text, nullable=True) # имя пользователя
    date =db.Column(db.String(100), nullable = True)
    link = db.Column(db.Text, nullable = True)

class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = True)
    link = db.Column (db.Text, nullable =True)

# Модель сообщений  - отображение таблицы massege в БД 
__tablename__ = 'massege'
class Massege(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id -сообщения
    id_progect = db.Column(db.Integer)# id проекта
    id_folder = db.Column(db.Integer)# id верхнкй папки
    id_task = db.Column(db.Integer)# id задачи
    id_user = db.Column(db.Integer)# id юзера
    text = db.Column(db.Text)# текст сообщения
    kk = db.relationship('Users_Data', backref='massege', uselist=False) #Связываем таблицу 