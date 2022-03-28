# файл конфигурации 
import os

app_dir = os.path.abspath(os.path.dirname(__file__)) # путь файла для загрузки модуля 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # Задаем токен для генерации cookie
    SQLALCHEMY_TRACK_MODIFICATIONS = False # отключаем мадификацию

    SQLALCHEMY_DATABASE_URI = 'sqlite:///phoenix.db' #ссылка на Sql 


    ##### настройка Flask-Mail #####
    MAIL_SERVER = 'smtp.googlemail.com'#название сервеса почты
    MAIL_PORT = 587 #порт почты
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com' # логин, а именно почта 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'# пароль от почты 
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopementConfig(Config): # Конфишурация разработки
    DEBUG = True #состояние дебага

class TestingConfig(Config):# Конфиуграция для тестирования
    DEBUG = True #состояние дебага
    

class ProductionConfig(Config):#Конфигурация
    DEBUG = False #состояние дебага
