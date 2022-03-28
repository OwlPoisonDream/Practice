# сдесь находятся модели класса
from werkzeug.security import generate_password_hash,  check_password_hash # для создание хеша паролей
from flask_login import  UserMixin 
from app import db,login_manager


@login_manager.user_loader # загрузка пользователя
def load_user(user_id):
    return db.session.query(User).get(id)


# Модель User  - отображение таблицы users в БД 
class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key =True) #id
    email = db.Column(db.String(20), nullable=False) # эмаил
    password_hash = db.Column(db.String(100), nullable=False) # пароль
    name = db.Column(db.String(100), nullable=False) #ФИО
    nickname = db.Column(db.String(20), nullable=True) # прозвище
    link_vk = db.Column(db.String(50), nullable=True) # ссылка на вк
    inn = db.Column(db.String(12), nullable=True) # инн
    bank_details = db.Column(db.String(100), nullable=True) # реквезиты банка  
    bankName = db.Column(db.String(100), nullable=True) # название банка
    phone_number = db.Column(db.String(11), nullable=True) # номер телефона

    def __reduce_ex__(self): # id пользователя и его почта 
        return "<{}{}>".format(self.id, self.email)

    def check_password(self,  password): # проверка пароля от пользователя и хэш
        return check_password_hash(self.password_hash, password)
        
    def set_password(self, password):# ввод пароля в виде хеша 
	    self.password_hash = generate_password_hash(password)




# Модель Tasks  - отображение таблицы task в БД 
class Tasks(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)#id задачи
    idUser = db.Column(db.Integer)# id пользователя 
    idProject = db.Column(db.Integer)# id проекта
    nameTask = db.Column(db.String(255))# имя задачи
    descTask = db.Column(db.String(255))# Описание задачи
    timeTask = db.Column(db.String(255))# время выполнения
    manyTask = db.Column(db.String(255))# денги за задачу
    statusСompleted = db.Column(db.String(255))#статус выполненияы
    receipt = db.Column(db.Float)# проверка чека
    linkDisk = db.Column(db.String(255))# ссылка на диск

# Модель Project  - отображение таблицы projects в БД 
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)# id проекта
    projectName = db.Column(db.String(255))# имя проекта
    descProject = db.Column(db.String(255))# описание проекта 
    linkDisk = db.Column(db.String(255))# ссылка на гугл диск

