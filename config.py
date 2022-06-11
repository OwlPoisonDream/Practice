# файл конфигурации 
import os
from docxtpl import DocxTemplate # вставка данных в word 

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
    way_photo = 'app/static/photos/'
    way_task = 'app/static/workTemplates/'
    way_check = 'app/static/checkTemplates/'
    doc = DocxTemplate("app/static/wordTemplates/шаблон_договор.docx")# открываем шаблон договра
    doc_act = DocxTemplate("app/static/wordTemplates/шаблон_акт.docx")# открываем шаблон акта
    way_doc = "app/static/wordTemplates/"
    yad_pr_way = "/Феникс проекты/"
    yad_con = "/договора/"
    photo = 'static/photos/'
    


class DevelopementConfig(Config): # Конфигурация разработки
    DEBUG = True #состояние дебага

class TestingConfig(Config):# Конфиуграция для тестирования
    DEBUG = True #состояние дебага
    

class ProductionConfig(Config):#Конфигурация
    DEBUG = False #состояние дебага
