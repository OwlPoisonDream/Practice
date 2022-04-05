# файл конфигурации 
import os


app_dir = os.path.abspath(os.path.dirname(__file__)) # путь файла для загрузки модуля 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # Задаем токен для генерации cookie
    SQLALCHEMY_TRACK_MODIFICATIONS = False # отключаем модификацию SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///phoenix.db' #ссылка на SQL

    ##### настройка Flask-Mail #####
    ADMINS = ['fenix4dminproba@yandex.ru']
    MAIL_SERVER = 'smtp.yandex.com'#название сервиса почты
    MAIL_PORT = 465 #порт почты
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('fenix4dminproba@yandex.ru')# логин, а именно почта 
    MAIL_PASSWORD = os.environ.get('pmdufnoeqlwfnwbq')# пароль от почты 
    MAIL_DEFAULT_SENDER = MAIL_USERNAME #email отправителя
     
    


class DevelopementConfig(Config): # Конфигурация разработки
    DEBUG = True #состояние дебага

class TestingConfig(Config):# Конфиуграция для тестирования
    DEBUG = True #состояние дебага
    

class ProductionConfig(Config):#Конфигурация
    DEBUG = False #состояние дебага
